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
from api.models.ec.wishlist import Wishlist


def front_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)

    # Fetch all the featured comics throughout all the stores or depending
    # on the organization / store.
    try:
        featured_comics = Comic.objects.filter(
            product__is_available=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_featured=True,
        )
    
        if org_id > 0:
            featured_comics = featured_comics.filter(organization_id=org_id)
                
        if store_id > 0:
            featured_comics = featured_comics.filter(product__store_id=store_id)
    except Comic.DoesNotExist:
        featured_comics = None
    
    # Fetch all the new comics throghout all the stores or depending on the
    # organization / store.
    try:
        new_comics = Comic.objects.filter(
            product__is_available=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_new=True,
        )

        if org_id > 0:
            new_comics = new_comics.filter(organization_id=org_id)

        if store_id > 0:
            new_comics = new_comics.filter(product__store_id=store_id)
    except Comic.DoesNotExist:
        new_comics = None

    # Display the view with all our model information.
    return render(request, 'store_landpage/index.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'featured_comics': featured_comics,
        'new_comics': new_comics,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'home',
    })


def tos_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)

    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)

    # Display the view with all our model information.
    return render(request, 'store_landpage/tos.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'tos',
    })


def privacy_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_landpage/privacy.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'tos',
    })

