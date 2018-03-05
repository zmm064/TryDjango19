"""
Definition of urls for TryDjango19.
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', TryDjango19.views.home, name='home'),
    # url(r'^TryDjango19/', include('TryDjango19.TryDjango19.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/', include("posts.urls", namespace='posts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)