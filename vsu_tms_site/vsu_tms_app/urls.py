from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpattterns = [
    url(r'^$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
