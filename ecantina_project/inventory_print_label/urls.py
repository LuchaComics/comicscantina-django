from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/(\d+)/(\d+)/print_labels/comics$', views.print_labels_page),
)