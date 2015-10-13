from django.conf.urls import patterns, include, url
from store_landpage import views

urlpatterns = patterns('',
    # Main Aggregate Store
    url(r'^$', views.front_page),
    url(r'store$', views.front_page),
    url(r'landpage$', views.front_page),
    
    # Specific Store
    url(r'^(\d+)/$', views.front_page),
    url(r'^(\d+)/(\d+)/$', views.front_page),
)
