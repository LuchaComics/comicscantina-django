from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^inventory/webservice/add_to_cart$', views.ajax_add_to_cart),
)

