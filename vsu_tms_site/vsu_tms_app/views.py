from django.shortcuts import render

# Create your views here.

def index(req):
    render(req,'index.html')
