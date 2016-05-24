from django.conf.urls import patterns, include, url
from store_search import views


urlpatterns = patterns('',
    url(r'^search$', views.search_page, name='store_search'),
)

