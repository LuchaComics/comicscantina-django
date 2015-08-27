from django.conf.urls import patterns, include, url
from store_landpage.views import landpage

urlpatterns = patterns('',
    url(r'^$', landpage.front_page),
    url(r'^(\d+)$', landpage.front_page),
    url(r'^(\d+)/$', landpage.front_page),
    url(r'^(\d+)/store$', landpage.front_page),
    url(r'^(\d+)/landpage$', landpage.front_page),
)
