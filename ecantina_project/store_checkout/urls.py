from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^cart$', views.cart_page),
    url(r'^(\d+)/cart$', views.cart_page),
    url(r'^(\d+)/(\d+)/cart$', views.cart_page),
                       
    url(r'^checkout/shipping$', views.checkout_shipping_page),
    url(r'^(\d+)/checkout/shipping$', views.checkout_shipping_page),
    url(r'^(\d+)/(\d+)/checkout/shipping$', views.checkout_shipping_page),
)