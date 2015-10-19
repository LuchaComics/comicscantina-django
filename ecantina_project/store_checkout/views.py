import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt
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
        receipt = Receipt.objects.get_or_create_for_customer(customer)

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
        receipt = Receipt.objects.get_or_create_for_customer(customer)

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
        'page' : 'home',
    })