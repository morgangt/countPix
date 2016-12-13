from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'countPix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^click/', views.click),
    url(r'^show/', views.show),
)
