from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class TaskList(models.Model):
    date_valid_for = models.DateField()
    datetime_created = models.DateTimeField(auto_now=True)
    created_by_user_id = models.ForeignKey(User,on_delete=models.PROTECT)
    
class LookupTaskFrequency(models.Model):
    frequency_or_day = models.CharField(64)
    
class LookupTaskUrgency(models.Model):
    urgency = models.CharField(64)
    
class Staff(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.PROTECT)
    name = models.CharField(64)

class Role(models.Model):
    role_desc = models.CharField(64)
    
class Task(models.Model):
    task_desc = models.CharField(max_length=128)
    responsible_role_id = models.ForeignKey(Role,on_delete=models.SET_NULL)
    assigned_role_id = models.ForeignKey(Role,on_delete=models.SET_NULL)
    task_frequency_id = models.ForeignKey(LookupTaskFrequency,on_delete=models.PROTECT)
    task_urgency_id = models.ForeignKey(LookupTaskUrgency,on_delete=models.PROTECT)

class TaskListItem(models.Model):
    tasklist_id = models.ForeignKey(TaskList,on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task,on_delete=models.PROTECT)
    complete = models.BooleanField(default=False)
    notes = models.CharField(max_length=128)
    time_due = models.DateTimeField()

class StaffRole(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
