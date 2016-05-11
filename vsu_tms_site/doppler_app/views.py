from django.shortcuts import render
from django.http import JsonResponse

from StringIO import StringIO
import wave
import scipy.io.wavfile
import numpy as np
from datetime import datetime
from os import getcwd
from os.path import join, normpath


# Create your views here.
def index(request):
    return render(request,'index.html')

def upload_doppler(request):
    doppler_blob = request.FILES['audio']

    dest_file_handle = 'doppler_audio_samples/test_audio' + str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    dest_file_handle = normpath(join(getcwd(),dest_file_handle))
    destination = open(dest_file_handle, 'wb+')
    for chunk in doppler_blob.chunks():
        destination.write(chunk)
    destination.close()

    rate, wf = scipy.io.wavfile.read(dest_file_handle)

    return JsonResponse({'received':'true','saved':'false'}) 
