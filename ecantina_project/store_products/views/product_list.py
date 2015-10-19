import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.tag import Tag
from api.models.ec.promotion import Promotion
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt


def list_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    organization = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Fetch objects used for searching criteria.
    try:
        categories = Category.objects.all().order_by('category_id')
    except Category.DoesNotExist:
        categories = None

    try:
        brands = Brand.objects.all()
    except Brand.DoesNotExist:
        brands = None

    # Get the categories and select the current category.
    category_id = int(request.GET.get('category'))
    try:
        current_category = Category.objects.get(category_id=category_id)
        
        # Filter down the products based on the organization / store / category.
        products = None
        if current_category.parent_id is 0:
            products = Product.objects.filter(category__parent_id=1)
        else:
            products = Product.objects.filter(category_id=category_id)
        if organization:
            products = products.filter(organization=organization)
        if store:
            products = products.filter(store=store)

        prod_count = len(products)
    except Category.DoesNotExist:
        current_category = None
        products = None
        prod_count = 0
    except Product.DoesNotExist:
        products = None
        prod_count = 0

    return render(request, 'store_products/product_list/list.html',{
        'receipt': receipt,
        'customer': customer,
        'categories': categories,
        'current_category': current_category,
        'brands': brands,
        'org': organization,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
    })
