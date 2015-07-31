from django.conf.urls import patterns, include, url
from inventory_add_product.views import add_comic
from inventory_add_product.views import search_comic


urlpatterns = patterns('',
    # Comics - Add/Edit
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/product/(\d+)$', add_comic.comic_page),
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/list_products$', add_comic.list_products),
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/upload_cover$', add_comic.ajax_save_uploaded_cover),
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/add_product$', add_comic.ajax_add_product),
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/section_dropbox/(\d+)$', add_comic.ajax_sections_per_store),
                    
    # Comics - Delete
    url(r'^inventory/(\d+)/(\d+)/add/comic/(\d+)/delete/(\d+)$', add_comic.ajax_delete_comic),
                       
    # Comics - Search
    url(r'^inventory/(\d+)/(\d+)/add/comic$', search_comic.search_comics_page),
    url(r'^inventory/(\d+)/(\d+)/add/search_comics$', search_comic.ajax_search_comics),
)