import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def front_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Fetch all the featured comics throughout all the stores or depending
    # on the organization / store.
    try:
        featured_comics = Comic.objects.filter(
            product__is_listed=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_featured=True,
            product__organization__is_listed=True,
            product__store__is_listed=True,
        )
    
        if org:
            featured_comics = featured_comics.filter(organization=org)
                
        if store:
            featured_comics = featured_comics.filter(product__store=store)
    except Comic.DoesNotExist:
        featured_comics = None
    
    # Fetch all the new comics throghout all the stores or depending on the
    # organization / store.
    try:
        new_comics = Comic.objects.filter(
            product__is_listed=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_new=True,
        )

        if org:
            new_comics = new_comics.filter(organization=org)

        if store:
            new_comics = new_comics.filter(product__store=store)
    except Comic.DoesNotExist:
        new_comics = None

    # Display the view with all our model information.
    return render(request, 'store_landpage/index.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'featured_comics': featured_comics,
        'new_comics': new_comics,
        'org': org,
        'store': store,
        'page': 'home',
        'settings': settings,
    })


def tos_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Display the view with all our model information.
    return render(request, 'store_landpage/tos.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def privacy_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists
    
    # Display the view with all our model information.
    return render(request, 'store_landpage/privacy.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


