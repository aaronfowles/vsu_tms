from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_doppler/', views.upload_doppler, name='upload_doppler'),
]
