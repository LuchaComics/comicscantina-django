from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^inventory/register$', views.store_registration_page),
    url(r'^inventory/save_image$', views.store_save_image),
    url(r'^inventory/create_account$', views.create_account),
)

