from django.conf.urls import patterns, include, url
from store_products.views import product_list

urlpatterns = patterns('',
    url(r'^products/list$', product_list.list_page),
    url(r'^products/list/$', product_list.list_page),
    url(r'^products/list/0$', product_list.list_page),
    url(r'^products/list/0/$', product_list.list_page),
    url(r'^products/list/(\d+)$', product_list.list_page),
    url(r'^products/list/(\d+)/$', product_list.list_page),
    url(r'^(\d+)/products/list$', product_list.list_page),
    url(r'^(\d+)/products/list/$', product_list.list_page),
    url(r'^(\d+)/products/list/(\d+)$', product_list.list_page),
    url(r'^(\d+)/products/list/(\d+)/$', product_list.list_page),
    url(r'^store/(\d+)/products/list$', product_list.list_page),
    url(r'^store/(\d+)/products/list/$', product_list.list_page),
    url(r'^store/(\d+)/products/list/(\d+)$', product_list.list_page),
    url(r'^store/(\d+)/products/list/(\d+)/$', product_list.list_page),
)