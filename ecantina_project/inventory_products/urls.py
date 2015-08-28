from django.conf.urls import patterns, include, url
from inventory_products.views import search
from inventory_products.views import add_comic
from inventory_products.views import search_comic


urlpatterns = patterns('',
    # Comics - Add/Edit
    url(r'^inventory/(\d+)/(\d+)/add/comic$', search_comic.search_comics_page),
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/product/(\d+)$', add_comic.comic_page),
                       
    # Inventory List
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/list/comics$', search.product_search_page),
)