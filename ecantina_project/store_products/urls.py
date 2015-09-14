from django.conf.urls import patterns, include, url
from store_products.views import product_list
from store_products.views import product_details

urlpatterns = patterns('',
    #product isting
    url(r'^products/list$', product_list.list_page),
    url(r'^products/list/$', product_list.list_page),
    url(r'^products/list/(\d+)$', product_list.list_page),
    url(r'^products/list/(\d+)/$', product_list.list_page),
    url(r'^(\d+)/products/list$', product_list.list_page),
    url(r'^(\d+)/products/list/$', product_list.list_page),
    url(r'^(\d+)/products/list/(\d+)$', product_list.list_page),
    url(r'^(\d+)/products/list/(\d+)/$', product_list.list_page),
   #product details
    url(r'^(\d+)/products/details/(\d+)$', product_details.details_page),
    url(r'^(\d+)/products/details/(\d+)/$', product_details.details_page),

)