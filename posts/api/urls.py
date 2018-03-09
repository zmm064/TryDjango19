from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.PostListAPIView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.PostDetailAPIView.as_view(), name='detail'),
    #url(r'^(?P<slug>[\w-]+)/edit$', views.post_update, name='update'),
    #url(r'^create$', views.post_create),
    #url(r'^(?P<slug>[\w-]+)/delete$', views.post_delete, name='delete'),
]