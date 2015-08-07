from django.conf.urls import patterns, include, url
from inventory_checkout.views import pos_session
from inventory_checkout.views import pos_process
from inventory_checkout.views import pos_checkout

urlpatterns = patterns('',
    # Checkout Main
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/checkout$', pos_session.checkout_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/$', pos_process.checkout_page),

)