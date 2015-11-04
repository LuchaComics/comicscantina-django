from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^inventory/(\d+)/(\d+)/orders$', views.orders_page),
    url(r'^inventory/(\d+)/(\d+)/orders/(\d+)/$', views.order_details_page),
)