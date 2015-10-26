from django.conf.urls import patterns, include, url
from store_customer import views

urlpatterns = patterns('',
    url(r'my_account', views.my_account_page),
    url(r'^(\d+)/my_account$', views.my_account_page),
    url(r'^(\d+)/(\d+)/my_account$', views.my_account_page),
                       
    url(r'authentication', views.authentication_page),
    url(r'^(\d+)/authentication$', views.authentication_page),
    url(r'^(\d+)/(\d+)/authentication$', views.authentication_page),
)
