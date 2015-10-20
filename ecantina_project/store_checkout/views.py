import json
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, payment_was_flagged
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from inventory_base.forms.customerform import CustomerForm


def cart_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/cart/view.html',{
        'receipt': receipt,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'home',
    })


def checkout_shipping_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


def checkout_billing_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/billing/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


def checkout_shipping_method_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Lock out 'Shipping' option if a single product in the cart requires
    # in store pickup only.
    has_no_shipping = False
    for product in receipt.products.all():
        if product.has_no_shipping:
            has_no_shipping = True

    # Lock out 'Shipping' option if the organization does not support it.
    preference = OrgShippingPreference.objects.get_by_org_or_none(organization=org)
    if preference.is_pickup_only:
        has_no_shipping = True

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping_method/view.html',{
        'has_no_shipping': has_no_shipping,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


def checkout_payment_method_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/payment_method/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@csrf_exempt
def checkout_thank_you_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/thank_you/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })

@csrf_exempt
def checkout_cancel_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/cancel/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


def checkout_order_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Generate our URLs
    base_url = settings.SITE_DOMAIN_URL
    if org is not None and store is None:
        base_url += "/"+str(org.org_id)
    if org is not None and store is not None:
        base_url += "/"+str(org.org_id)+"/"+str(store.store_id)
    return_url = base_url+"/checkout/thank_you"
    cancel_url = base_url+"/checkout/cancel"

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(receipt.total_amount),
        "item_name": "Comic Book(s) Purchase, Receipt #"+str(receipt.receipt_id),
        "invoice": str(receipt.receipt_id),
        "notify_url": "/checkout/" + reverse('paypal-ipn'),
        "return_url": return_url,
        "cancel_return": cancel_url,
        "custom": "perform_receipt_checkout",  # Custom command to correlate to some function later (optional)
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/order/view.html',{
        'paypal_form': form,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })
