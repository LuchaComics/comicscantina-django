from django.conf.urls import patterns, include, url
from mobile_pos.views import pos_login
from mobile_pos.views import pos_dashboard
from mobile_pos.views import pos_cart
from mobile_pos.views import pos_search_customer


urlpatterns = patterns('',
    url(r'^mobile/pos/login$', pos_login.login_page),
    url(r'^mobile/pos/(\d+)/dashboard$', pos_dashboard.dashboard_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/$', pos_cart.cart_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/search_customer$', pos_search_customer.search_customer_page),
)