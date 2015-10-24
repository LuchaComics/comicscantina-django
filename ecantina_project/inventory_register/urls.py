from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/register/step1$', views.step1_page),
)