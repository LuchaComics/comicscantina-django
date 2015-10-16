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
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt


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
    organization = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_customer(customer)

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
        'receipt': receipt,
        'customer': customer,
        'org': organization,
        'store': store,
        'categories': categories,
        'comic': comic,
        'product': product,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
    })
