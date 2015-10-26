from django.conf.urls import patterns, include, url
from store_customer import views

urlpatterns = patterns('',
    url(r'customer/my_account', views.my_account_page),
    url(r'^(\d+)/customer/my_account$', views.my_account_page),
    url(r'^(\d+)/(\d+)/customer/my_account$', views.my_account_page),
                       
    url(r'customer/authentication', views.authentication_page, name="authentication"),
    url(r'^(\d+)/customer/authentication$', views.authentication_page),
    url(r'^(\d+)/(\d+)/customer/authentication$', views.authentication_page),
)
