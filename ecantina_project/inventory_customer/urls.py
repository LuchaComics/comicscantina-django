from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Customers
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/customers$', views.customers_page),
    url(r'^inventory/(\d+)/(\d+)/add_customer$', views.add_customer_page),
)