from django.conf.urls import url
from django.contrib import admin

from .views import comment_thread

urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    
]
