from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from StringIO import StringIO
import wave
import scipy.io.wavfile
from scipy import signal
import numpy as np
from datetime import datetime
from os import getcwd
from os.path import join, normpath

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
    amplitude_threshold = 0.2
    gradient_threshold = 0.6
    running_lag = 0
    running_lag_threshold = 20000
    backstep_offset = 1000
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
    for wf_wave in wf_list:
        temp_dict = {}

        temp_dict['mean'] = wf_wave.mean()
        energy = 0
        for i in range(0,len(wf_wave)-1):
            energy += wf_wave[i]*wf_wave[i]
        temp_dict['raw_energy'] = energy

        context['waves'].append(temp_dict)

    context['num_waveforms'] = num_points

    return JsonResponse(context)
