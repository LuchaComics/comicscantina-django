from django.conf.urls import patterns, include, url
from store_landpage.views import aggregate
from store_landpage.views import specific

urlpatterns = patterns('',
    # Main Aggregate Store
    url(r'^$', aggregate.front_page),
    
    # Specific Store
    url(r'^(\d+)$', specific.front_page),
    url(r'^(\d+)/$', specific.front_page),
    url(r'^(\d+)/store$', specific.front_page),
    url(r'^(\d+)/landpage$', specific.front_page),
)
