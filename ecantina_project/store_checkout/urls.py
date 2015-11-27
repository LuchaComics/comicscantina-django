from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^cart$', views.cart_page),
    url(r'^checkout/shipping$', views.checkout_shipping_page),
    url(r'^checkout/billing$', views.checkout_billing_page),
    url(r'^checkout/shipping_method$', views.checkout_shipping_method_page),
    url(r'^checkout/payment_method$', views.checkout_payment_method_page),
    url(r'^checkout/order$', views.checkout_order_page),
    url(r'^checkout/thank_you/(\d+)$', views.checkout_thank_you_page),
    url(r'^checkout/cancel$', views.checkout_cancel_page),
                       
    # PayPal
    url(r'^checkout/paypal/', include('paypal.standard.ipn.urls')),
)