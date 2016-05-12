from django.shortcuts import render
from django.http import JsonResponse

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
    print('upload doppler called')
    doppler_blob = request.FILES['audio']

    dest_file_handle = 'doppler_audio_samples/' + str(datetime.now().strftime('%Y-%m-%d_%H-%M'))
    dest_file_handle = normpath(join(getcwd(),dest_file_handle))
    destination = open(dest_file_handle, 'wb+')
    for chunk in doppler_blob.chunks():
        destination.write(chunk)
    destination.close()

    rate, wf = scipy.io.wavfile.read(dest_file_handle)

    wf = wf[:,0]

    # Band-pass filtering
    print('find waveform called')
    nyq = 0.5 * 44100
    cutoff = 250 / nyq
    b, a = signal.butter(4,cutoff,'highpass')
    wf = signal.lfilter(b, a, wf)
    cutoff = 1000 / nyq
    b, a = signal.butter(4,cutoff,'lowpass')
    wf = signal.lfilter(b, a, wf)
    # Normalise waveform
    peak_amplitude = wf.max()
    wf = wf / float(peak_amplitude)
    # calculate magnitude
    wf_for_grad = [i if i > 0 else i*(-1) for i in wf]
    # Calculate gradients and normalise them
    wf_grad = np.gradient(wf_for_grad)
    peak_gradient = wf_grad.max()
    wf_grad = wf_grad / float(peak_gradient)
    # Waveform finding logic
    start_indices = []
    amplitude_threshold = 0.3
    gradient_threshold = 0.3
    running_lag = 0
    running_lag_threshold = 10000
    for i in range(0,len(wf)):
        if (wf[i] > amplitude_threshold and wf_grad[i] > gradient_threshold and running_lag >= running_lag_threshold):
            start_indices.append(1)
            running_lag = 0
        else:
            start_indices.append(0)
            running_lag += 1

    context = {}
    context['sample_length_secs'] = len(wf) / float(rate)

    num_points = 0
    for i in range(0,len(start_indices)):
        if (start_indices[i] is not 0):
            num_points += 1
    context['num_waveforms'] = num_points

    return render(request,'results.html', context)
