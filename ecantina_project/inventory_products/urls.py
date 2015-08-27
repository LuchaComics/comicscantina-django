from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',                       
    # Inventory List
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/list/comics$', views.product_search_page),
)