from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/(\d+)/(\d+)/help$', views.help_page),
    url(r'^inventory/(\d+)/(\d+)/help/save_image$', views.ajax_save_image),
    url(r'^inventory/(\d+)/(\d+)/help/save_data$', views.ajax_save_data),
)