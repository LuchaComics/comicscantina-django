from django.conf.urls import patterns, include, url
from store_landpage import views

urlpatterns = patterns('',
    # Main Aggregate Store
    url(r'^$', views.front_page, name='store_landpage'),
    url(r'landpage$', views.front_page),
                       
    # Misc
    url(r'tos$', views.tos_page, name='store_tos'),
                       
    # Specific Store
    url(r'^(\d+)/$', views.front_page),
    url(r'^(\d+)/(\d+)/$', views.front_page),
)
