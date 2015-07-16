from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^inventory/webservice/json$', views.json_rpc_view),
)

