from django.conf.urls import patterns, include, url
from store_products.views import product_list
from store_products.views import product_details

urlpatterns = patterns('',
    #product isting
    url(r'^products/grid$', product_list.list_page),
    url(r'^(\d+)/products/grid$', product_list.list_page),
    url(r'^(\d+)/(\d+)/products/grid$', product_list.list_page),
   #product details
    url(r'^(\d+)/products/details/(\d+)$', product_details.details_page),
    url(r'^(\d+)/products/details/(\d+)/$', product_details.details_page),

)