from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse

from datetime import date, datetime

from .models import TaskListItem, Task, Staff, Role, LookupTaskUrgency, AuditLog, TaskList

# Login page
def user_login(req):
    return render(req,"login.html")

# Verify login  page
def verify(req):
    context = {}
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(username=username, password=password)
    context['response'] = HttpResponse()
    if user is not None:
        if user.is_active:
            login(req,user)
            return render(req, "index.html", context)
        else:
            return render(req,"login.html", context)
    else:
        context['response'].content = "Credentials do not match existing user"
    return render(req,"login.html", context)


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
        temp_dict['tasklist_id'] = tasklist_item.tasklist_id.id
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
        task_obj = Task.objects.get(id=tasklist_item.task_id.id)
        if (task_obj.assigned_role_id.id == role.id):
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


# Submit task completion
@login_required()
def task_completed(req):
    context = {}
    tasklistitem_id = req.POST['tasklistitem_id']
    user_id = req.user
    tasklistitem = TaskListItem.objects.get(id=tasklistitem_id)
    tasklistitem.complete = True
    log = AuditLog(user_id=user_id, tasklist_id=tasklistitem)
    tasklistitem.save()
    log.save()
    return HttpResponse("OK")

# Create TaskList
@login_required()
def create_task_list(req):
    context = {}
    username = User.objects.get(username='dev')
    if(req.user is not None):
        username = req.user
    day = date.today()
    if (TaskList.objects.filter(date_valid_for=day)):
        return HttpResponse("Denied")
    new_list = TaskList.objects.create(date_valid_for=day,created_by_user_id=username)
    tasks = Task.objects.all()
    set_weekly = True if day.isoweekday()==1 else False
    set_monthly = True if day.day==1 else False
    set_annually = True if set_monthly and day.month==1 else False 
    to_commit = []
    for task in tasks:
        if (set_annually and task.task_frequency_id == 'annually'):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,12,31))
            continue
        if (set_monthly and task.task_frequency_id == 'monthly'):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,(day.month+1),day.day))
            continue
        if (set_weekly and task.task_frequency_id == 'weekly'):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,(day.day+7)))
            continue
        if (task.task_frequency_id == 'monday' and day.isoweekday() == 1):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue 
        if (task.task_frequency_id == 'tuesday' and day.isoweekday() == 2):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue
        if (task.task_frequency_id == 'wednesday' and day.isoweekday() == 3):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue
        if (task.task_frequency_id == 'thursday' and day.isoweekday() == 4):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue
        if (task.task_frequency_id == 'friday' and day.isoweekday() == 5):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue
        if (task.task_frequency_id == 'daily' and day.isoweekday() not in [6,7]):
            TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,17))
            continue
        if (str(task.task_frequency_id) == 'hourly' and day.isoweekday() not in [6,7]):
            to_commit.append('hourly')
            for hour in range(8,18):
                TaskListItem.objects.create(tasklist_id=new_list,task_id=task,time_due=datetime(day.year,day.month,day.day,hour))
            continue

    return HttpResponse(str(','.join(to_commit)))

def test_script():
    return 'test_script called'
