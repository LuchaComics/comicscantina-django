from django.conf.urls import patterns, include, url
from inventory_add_product.views import add_comic
from inventory_add_product.views import search_comic


urlpatterns = patterns('',
    # Comics - Add/Edit
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/product/(\d+)$', add_comic.comic_page),
                    
    # Comics - Search
    url(r'^inventory/(\d+)/(\d+)/add/comic$', search_comic.search_comics_page),
)