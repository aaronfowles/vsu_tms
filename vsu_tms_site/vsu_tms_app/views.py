from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Landing page
def index(req):
    return render(req,'index.html')

# Home page
@login_required()
def home(req):
    return render(req, 'home.html')

# My Tasks page
@login_required()
def my_tasks(req):
    return render(req,'my_tasks.html')

# Daily Management Page
@login_required()
def daily_management(req):
    return render(req,'daily_management.html')
