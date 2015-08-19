from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/(\d+)/(\d+)/pulllist$', views.pulllist_page),
)