import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.product import Product

def details_page(request, org_id=0, store_id=0, product_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    product_id = int(product_id)
    if product_id is 0:
        if org_id is not 0 and store_id is 0:
            product_id = org_id
        if org_id is not 0 and store_id is not 0:
            product_id = store_id

    # Fetch the Organization / Store.
    try:
        organization = Organization.objects.get(org_id=org_id)
    except Organization.DoesNotExist:
        organization = None
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        store = None
    
    # Fetch objects used for searching criteria.
    try:
        categories = Category.objects.all().order_by('category_id')
    except Category.DoesNotExist:
        categories = None

    # Fetch the product details
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        product = None
    try:
        comic = Comic.objects.get(product__product_id=product_id)
    except Comic.DoesNotExist:
        comic = None

    return render(request, 'store_products/product_details/details.html',{
        'org': organization,
        'store': store,
        'categories': categories,
        'comic': comic,
        'product': product,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
    })
