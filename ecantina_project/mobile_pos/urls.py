from django.conf.urls import patterns, include, url
from mobile_pos.views import pos_login
from mobile_pos.views import pos_dashboard
from mobile_pos.views import pos_cart
from mobile_pos.views import pos_scanner
from mobile_pos.views import pos_checkout
from mobile_pos.views import pos_remove_product


urlpatterns = patterns('',
    url(r'^mobile/pos/login$', pos_login.login_page),
    url(r'^mobile/pos/(\d+)/dashboard$', pos_dashboard.dashboard_page),
    url(r'^mobile/pos/(\d+)/remove_product$', pos_remove_product.remove_product_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/$', pos_cart.cart_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/product_scanner$', pos_scanner.scanner_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/checkout$', pos_checkout.checkout_page),
)