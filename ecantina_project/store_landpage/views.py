import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic


def front_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    try:
        org = Organization.objects.get(org_id=org_id)
    except Organization.DoesNotExist:
        org = None
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        store = None

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

    return render(request, 'store_landpage/index.html',{
        'featured_comics': featured_comics,
        'new_comics': new_comics,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'home',
    })