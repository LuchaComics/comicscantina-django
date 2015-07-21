from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^inventory/register$', views.store_registration_page, name='register'),
    url(r'^inventory/save_image$', views.ajax_store_save_image),
    url(r'^inventory/create_account$', views.ajax_create_account),
    url(r'^inventory/registered_successful$', views.store_registation_successful_page, name='registered_successful'),
)

