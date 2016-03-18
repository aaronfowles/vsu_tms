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
    context['all_tasklist_items'] = all_incomplete
    return render(req, 'home.html', context)

# My Tasks page
@login_required()
def my_tasks(req):
    context = {}
    user = req.user.id
    staff = Staff.objects.get(user_id=user).id
    role = Staff.objects.get(id=staff).role_id
    
    context['my_tasks_items'] = []

    incomplete_tasks = TaskListItem.objects.filter(complete=False)
    tasks_assigned_to_role = Task.objects.filter(assigned_role_id=role)

    task_ids_assigned_to_role = [task.id for task in tasks_assigned_to_role]

    for task in incomplete_tasks:
        temp_dict = {}
        if task.task_id.id in task_ids_assigned_to_role:
            temp_dict['tasklist_id'] = task.tasklist_id
            temp_dict['task_id'] = task.task_id
            urgency = Task.objects.get(id=task.task_id.id).task_urgency_id
            urgency = LookupTaskUrgency.objects.get(id=urgency.id).urgency
            temp_dict['urgency'] = urgency
            temp_dict['task_desc'] = Task.objects.get(id=task.task_id.id).task_desc
            temp_dict['time_due'] = task.time_due
            context['my_tasks_items'].append(dict(temp_dict))

    return render(req,'my_tasks.html', context)

# Daily Management Page
@login_required()
def daily_management(req):
    return render(req,'daily_management.html')
