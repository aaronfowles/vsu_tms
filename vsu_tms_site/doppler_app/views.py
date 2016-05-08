from django.shortcuts import render
from django.http import JsonResponse

from StringIO import StringIO
import wave
import scipy.io.wavfile
import numpy as np

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload_doppler(request):
    doppler_blob = request.FILES['audio']
    
    destination = open('test_audio.wav', 'wb+')
    for chunk in doppler_blob.chunks():
        destination.write(chunk)
    destination.close()

    return JsonResponse({'received':'true','saved':'false'}) 
