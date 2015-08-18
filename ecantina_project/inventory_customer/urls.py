from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Customers
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/customers$', views.customers_page),
    url(r'^inventory/(\d+)/(\d+)/customers/refresh_table$', views.ajax_refresh_table),
    url(r'^inventory/(\d+)/(\d+)/customers/delete$', views.ajax_delete_customer),
    url(r'^inventory/(\d+)/(\d+)/add_customer$', views.add_customer_page),
    url(r'^inventory/(\d+)/(\d+)/add_customer/submit$', views.ajax_add_customer),
)