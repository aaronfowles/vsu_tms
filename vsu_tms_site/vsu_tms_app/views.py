from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import TaskListItem, Task


# Landing page
def index(req):
    return render(req,'index.html')

# Home page
@login_required()
def home(req):
    context = {}
    all_incomplete = TaskListItem.objects.filter(complete=False).select_related()
    context['all_tasklist_items'] = all_incomplete
    return render(req, 'home.html', context)

# My Tasks page
@login_required()
def my_tasks(req):
    context = {}
    user = req.user.id
    staff = Staff.objects.get(user_id=user).id
    role = Staff.objects.get(staff_id=staff).id
    all_incomplete_and_for_role = TaskListItem.filter(complete=False).select_related().filter(role_id=role)
    context['my_tasks_items'] = all_incomplete_and_for_role
    return render(req,'my_tasks.html', context)

# Daily Management Page
@login_required()
def daily_management(req):
    return render(req,'daily_management.html')
