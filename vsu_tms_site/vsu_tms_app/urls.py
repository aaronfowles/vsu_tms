from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^verify/', views.verify, name='verify'),
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^my_tasks/', views.my_tasks, name='my_tasks'),
    url(r'^daily_management/', views.daily_management, name='daily_management'),
    url(r'^task_completed/', views.task_completed, name='task_completed'),
    url(r'^create_task_list',views.create_task_list, name='create_task_list'),
    url(r'^logout', views.user_logout, name='user_logout'),
    url(r'^register', views.user_register, name='user_register'),
    url(r'^send_registration_request', views.send_registration_request, name='send_registration_request'),
    url(r'^task_not_completed', views.task_not_completed, name='task_not_completed'),
    url(r'^task_pending', views.task_pending, name='task_pending'),
    url(r'^role_tasks/(?P<role_id>\w+/$)',views.role_tasks, name='role_tasks'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
