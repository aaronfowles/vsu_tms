from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

class TaskList(models.Model):
    date_valid_for = models.DateField()
    datetime_created = models.DateTimeField(auto_now=True)
    created_by_user_id = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date_valid_for)
    
class LookupTaskFrequency(models.Model):
    frequency_or_day = models.CharField(max_length=64)

    def __str__(self):
        return self.frequency_or_day
    
class LookupTaskUrgency(models.Model):
    urgency = models.CharField(max_length=64)

    def __str__(self):
        return self.urgency
    
class Staff(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)

    def __str__(self):
        return self.name

class Role(models.Model):
    role_desc = models.CharField(max_length=64)
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.role_desc

class Task(models.Model):
    task_desc = models.CharField(max_length=128)
    responsible_role_id = models.ForeignKey(Role,related_name='responsible',on_delete=models.CASCADE)
    assigned_role_id = models.ForeignKey(Role,related_name='assigned',on_delete=models.CASCADE)
    task_frequency_id = models.ForeignKey(LookupTaskFrequency,on_delete=models.PROTECT)
    task_urgency_id = models.ForeignKey(LookupTaskUrgency,on_delete=models.PROTECT)

    def __str__(self):
        return self.task_desc

class TaskListItem(models.Model):
    tasklist_id = models.ForeignKey(TaskList,on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task,on_delete=models.PROTECT)
    complete = models.BooleanField(default=False)
    notes = models.CharField(max_length=128, blank=True)
    time_due = models.DateTimeField()

    def __str__(self):
        return str(self.task_id)

class StaffRole(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.staff_id) + str(self.role_id)

class AuditLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now=True)
    tasklist_id = models.ForeignKey(TaskListItem, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user_id) + str(self.timestamp) + str(self.tasklist_id)
