from django.conf.urls import patterns, include, url
from store_base import views


urlpatterns = patterns('',
    url(r'^403$', views.http_403_page, name='403_error'),
    url(r'^404$', views.http_404_page, name='404_error'),
                       
    url(r'^storefront/([a-z]+)/$', views.storefront_redirect),
)