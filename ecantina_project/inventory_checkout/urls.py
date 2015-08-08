from django.conf.urls import patterns, include, url
from inventory_checkout.views import pos_session
from inventory_checkout.views import pos_customer
from inventory_checkout.views import pos_item
from inventory_checkout.views import pos_receipt

urlpatterns = patterns('',
    # Checkout Main
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/checkout$', pos_session.checkout_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/customer$', pos_customer.checkout_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items$', pos_item.checkout_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/receipt$', pos_receipt.checkout_page),
)