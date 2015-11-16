from django.conf.urls import patterns, include, url
from store_help import views

urlpatterns = patterns('',
    url(r'^help$', views.help_page, name='store_help'),
    url(r'^(\d+)/help$', views.help_page),
    url(r'^(\d+)/(\d+)/help$', views.help_page),
)

