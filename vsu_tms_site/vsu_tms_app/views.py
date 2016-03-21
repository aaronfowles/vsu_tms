from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import TaskListItem, Task, Staff, Role, LookupTaskUrgency


# Landing page
def index(req):
    return render(req,'index.html')

# Home page
@login_required()
def home(req):
    context = {}
    all_incomplete = TaskListItem.objects.filter(complete=False).select_related()
    context['all_tasklist_items'] = []
    for tasklist_item in all_incomplete:
        temp_dict = {}
        temp_dict['tasklistitem_id'] = tasklist_item.id
        temp_dict['time_due'] = tasklist_item.time_due
        temp_dict['task_id'] = tasklist_item.task_id.id
        task_obj = Task.objects.get(id=tasklist_item.task_id.id)
        temp_dict['task_desc'] = task_obj.task_desc
        temp_dict['assigned_role'] = task_obj.assigned_role_id
        urgency = LookupTaskUrgency.objects.get(id=task_obj.task_urgency_id.id)
        temp_dict['urgency'] = urgency
        context['all_tasklist_items'].append(dict(temp_dict))
    return render(req, 'home.html', context)

# My Tasks page
@login_required()
def my_tasks(req):
    context = {}
    user = req.user.id
    staff = Staff.objects.get(user_id=user).id
    role = Staff.objects.get(id=staff).role_id
    
    context['my_tasks_items'] = []

    all_incomplete = TaskListItem.objects.filter(complete=False).select_related()
    for tasklist_item in all_incomplete:
        temp_dict = {}
        temp_dict['tasklistitem_id'] = tasklist_item.id
        temp_dict['tasklist_id'] = tasklist_item.tasklist_id.id
        temp_dict['time_due'] = tasklist_item.time_due
        temp_dict['task_id'] = tasklist_item.task_id.id
        task_obj = Task.objects.get(id=tasklist_item.task_id.id)
        temp_dict['task_desc'] = task_obj.task_desc
        temp_dict['assigned_role'] = task_obj.assigned_role_id
        urgency = LookupTaskUrgency.objects.get(id=task_obj.task_urgency_id.id)
        temp_dict['urgency'] = urgency
        context['my_tasks_items'].append(dict(temp_dict))

    return render(req,'my_tasks.html', context)

# Daily Management Page
@login_required()
def daily_management(req):
    return render(req,'daily_management.html')
