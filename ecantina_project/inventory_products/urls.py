from django.conf.urls import patterns, include, url
from inventory_products.views import comic
from inventory_products.views import search
from inventory_products.views import search_comic


urlpatterns = patterns('',
    # Comics - Add/Edit
    url(r'^inventory/(\d+)/(\d+)/comics$', search_comic.search_comics_page),
    url(r'^inventory/(\d+)/(\d+)/comic/(\d+)/product/(\d+)$', comic.comic_page),
                       
    # Inventory List
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/products$', search.product_search_page),
)