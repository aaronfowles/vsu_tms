from django.contrib import admin

# Register your models here.
from .models import Task,TaskList,TaskListItem,LookupTaskFrequency,LookupTaskUrgency,Staff,Role,StaffRole,AuditLog

admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(TaskListItem)
admin.site.register(LookupTaskFrequency)
admin.site.register(LookupTaskUrgency)
admin.site.register(Staff)
admin.site.register(Role)
admin.site.register(StaffRole)
admin.site.register(AuditLog)
