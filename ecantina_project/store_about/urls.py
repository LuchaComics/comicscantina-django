from django.conf.urls import patterns, include, url
from store_about.views import about

urlpatterns = patterns('',
    url(r'^about$', about.about_page),
    url(r'^about/$', about.about_page),
    url(r'^(\d+)/about$', about.about_page),
    url(r'^(\d+)/about/$', about.about_page),
    url(r'^store/(\d+)/about$', about.about_page),
    url(r'^store/(\d+)/about/$', about.about_page),
)