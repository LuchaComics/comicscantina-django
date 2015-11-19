import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from api.models.ec.organization import Organization
from api.models.ec.store import Store

def about_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    try:
        organization = Organization.objects.get(org_id=org_id)
    except Organization.DoesNotExist:
        organization = None
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        store = None

    # Fetch either all the stores within the organization or fetch the
    # individual store at the 'store_id' value.
    stores = None
    if store_id > 0:
        stores = Store.objects.filter(store_id=store_id)
    else:
        stores = Store.objects.filter(organization=organization)

    return render(request, 'store_about/about.html',{
        'org' : organization,
        'store': store,
        'stores' : stores,
        'page' : 'about',
    })
