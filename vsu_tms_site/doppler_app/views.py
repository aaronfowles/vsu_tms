from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from StringIO import StringIO
import wave
import scipy.io.wavfile
from scipy import signal
import numpy as np
from datetime import datetime
from os.path import join, normpath, isfile

from math import sqrt
from os import listdir, getcwd
from matplotlib import pyplot as plt
from matplotlib import figure as fig
from tempfile import TemporaryFile
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
import pandas as pd
import cPickle

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload_doppler(request):
    doppler_blob = request.FILES['audio']

    dest_file_handle = 'doppler_audio_samples/' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    dest_file_handle = normpath(join(getcwd(),dest_file_handle))
    destination = open(dest_file_handle, 'wb+')
    for chunk in doppler_blob.chunks():
        destination.write(chunk)
    destination.close()

    rate, wf = scipy.io.wavfile.read(dest_file_handle)

    wf = wf[:,0]

    # Band-pass filtering
    sampling_frequency = 44100
    nyq = 0.5 * 44100
    cutoff = 250 / nyq
    b, a = signal.butter(4,cutoff,'highpass')
    wf = signal.lfilter(b, a, wf)
    cutoff = 1000 / nyq
    b, a = signal.butter(4,cutoff,'lowpass')
    wf = signal.lfilter(b, a, wf)
    # Normalise waveform
    peak_amplitude = wf.max()
    wf_normed = wf / float(peak_amplitude)
    # calculate magnitude
    wf_for_grad = [i if i > 0 else i*(-1) for i in wf_normed]
    # Calculate gradients and normalise them
    wf_grad = np.gradient(wf_for_grad)
    peak_gradient = wf_grad.max()
    wf_grad = wf_grad / float(peak_gradient)
    # Waveform finding logic
    start_indices = []
    amplitude_threshold = 0.4
    gradient_threshold = 0.6
    running_lag_threshold = 20000
    backstep_offset = 1000
    running_lag = running_lag_threshold - backstep_offset
    for i in range(0,len(wf)):
        if (wf_normed[i] > amplitude_threshold and wf_grad[i] > gradient_threshold and running_lag >= running_lag_threshold):
            start_indices[i-backstep_offset] = 1
            running_lag = 0
        else:
            start_indices.append(0)
            running_lag += 1

    context = {}
    context['sample_length_secs'] = len(wf) / float(rate)

    num_points = 0
    true_points = {}
    for i in range(0,len(start_indices)):
        if (start_indices[i] is not 0):
            num_points += 1
            true_points[str(i)] = True
    start_stop_list = true_points.keys()
    wf_start_stop_points = []
    start_stop_list = [int(i) for i in start_stop_list]
    start_stop_list = sorted(start_stop_list)

    for i in range(0,len(start_stop_list)):
        if (i < len(start_stop_list)-1):
            wf_start_stop_points.append((start_stop_list[i], start_stop_list[i+1]-1))
    wf_list = []

    for pair in wf_start_stop_points:
        wf_list.append(wf[pair[0]:pair[1]])

    context['waves'] = []
    for wf_segment in wf_list:
        wave_metrics = {}
        wave_metrics['wf'] = wf_segment
        wave_metrics['mean'] = wf_segment.mean()
        energy = 0
        for i in range(0,len(wf_segment)-1):
            energy += wf_segment[i]*wf_segment[i]
        wave_metrics['raw_energy'] = energy
        wave_metrics['raw_power'] = energy / float(len(wf_segment))
        wave_metrics['raw_variance'] = wf_segment.var()
        wave_metrics['raw_RMS'] = sqrt(np.absolute(wave_metrics['raw_power']))
        wf_segment_gradient = np.absolute(np.gradient(np.absolute(wf_segment)))
        wave_metrics['raw_gradient_variance'] = wf_segment_gradient.var() 
        wave_metrics['raw_gradient_mean'] = wf_segment_gradient.mean()
        wave_metrics['raw_gradient_median'] = np.median(wf_segment_gradient)
        wave_metrics['length_secs'] = len(wf_segment) / float(44100)
        normalised_wf_segment = wf_segment / float(wf_segment.max())
	energy = 0
        for i in range(0,len(normalised_wf_segment)-1):
            energy += normalised_wf_segment[i]*normalised_wf_segment[i]
        wave_metrics['normalised_energy'] = energy
        wave_metrics['normalised_power'] = energy / float(len(normalised_wf_segment))
        wave_metrics['normalised_variance'] = normalised_wf_segment.var()
        wave_metrics['normalised_RMS'] = sqrt(wave_metrics['normalised_power'])
        normalised_wf_segment_gradient = np.absolute(np.gradient(np.absolute(normalised_wf_segment)))
        wave_metrics['normalised_gradient_variance'] = normalised_wf_segment_gradient.var() 
        wave_metrics['normalised_gradient_mean'] = normalised_wf_segment_gradient.mean()
        wave_metrics['normalised_gradient_median'] = np.median(normalised_wf_segment_gradient)
        #FFT
        T = 1 / float(sampling_frequency)
        N = len(wf_segment)
        x = np.linspace(0.0, 1.0/(2.0*T), N/2)
        ft = np.fft.fft(wf_segment)
        freq = np.fft.fftfreq(len(wf_segment),T)
        freq = freq[freq >= 0]
        zipped = zip(freq,20*(np.log10(np.abs(ft[0:N/2]))))
        for i in range(0,28):
            freq_sum = 0
            power_sum = 0
            for j in range(0,150):
                freq_sum += zipped[i*150 + j][0]
                power_sum += zipped[i*150 + j][1]
            freq_mean = int(round(freq_sum / float(150), -2))
            power_mean = power_sum / float(150)
            wave_metrics[str(i)] = power_mean
        context['waves'].append(wave_metrics)
        
    counter = 0
    img_store = {}
    final_df = pd.DataFrame()
    for w in context['waves']:
        for k, v in w.iteritems():
            if (k == 'wf'):
                continue
            final_df.loc[counter, k] = v
        final_df.loc[counter, 'class'] = 'brachial'
        data, freqs, bins, im = plt.specgram(w['wf'], Fs=sampling_frequency)
        with TemporaryFile() as tmpfile:
            plt.savefig(tmpfile,bbox_inches='tight') # File position is at the end of the file.
            tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
            im = Image.open(tmpfile)
            npa = np.asarray(im) # array indexed by [y][x] where [0][0] is bottom-left corner (cartesian)
        img_store[str(counter)] = npa[:200,:200,0]
        # Extract specgram features and insert into dataframe
        bands = 50
        for band in range(0,bands):
            lower_freq = (img_store[str(counter)].shape[0] / bands) * band
            higher_freq = (img_store[str(counter)].shape[0] / bands) * (band+1)
            colname = 'energy_band_' + str(band)
            final_df.loc[counter, colname] = img_store[str(counter)][lower_freq:higher_freq,:].sum() / (img_store[str(counter)].shape[0] * (higher_freq - lower_freq))
        counter += 1
        
    mod_path = join(getcwd(),'doppler_app','classifier.pkl')
    with open(mod_path, 'rb') as fid:
        model = cPickle.load(fid)
    X = final_df.ix[:,final_df.columns != 'class']
    predictions = model.predict(X)
    convert_dict = {'brachial':0.0,'carotid':1.0}
    running_total = 0.0
    for p in predictions:
	running_total += float(convert_dict[str(p)])
    context = {}
    prediction_float = running_total / float(len(predictions))
    prediction = ''
    if (prediction_float > 0.5):
        prediction = 'Carotid'
    else:
        prediction = 'Brachial'
    context['prediction'] = prediction
    return JsonResponse(context)
