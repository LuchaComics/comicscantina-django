from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/(\d+)/(\d+)/help$', views.help_page),
)