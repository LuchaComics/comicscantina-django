from django.conf.urls import patterns, include, url
from store_products.views import product_list
from store_products.views import product_details

urlpatterns = patterns('',
    # Product Listing
    #----------------------
    url(r'^products/grid$', product_list.list_page),
    url(r'^(\d+)/products/grid$', product_list.list_page),
    url(r'^(\d+)/(\d+)/products/grid$', product_list.list_page),
                       
    # Product Details
    #----------------------
    url(r'^products/(\d+)/$', product_details.details_page),
    url(r'^(\d+)/products/(\d+)/$', product_details.details_page),
    url(r'^(\d+)/(\d+)/products/(\d+)/$', product_details.details_page),
)