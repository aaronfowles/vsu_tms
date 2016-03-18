from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^my_tasks/', views.my_tasks, name='my_tasks'),
    url(r'^daily_management/', views.daily_management, name='daily_management'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
