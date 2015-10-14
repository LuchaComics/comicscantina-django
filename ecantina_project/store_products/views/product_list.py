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


def list_page(request, org_id=0, store_id=0):
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


    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        prod_page = paginator.page(page)
    except PageNotAnInteger:
        prod_page = paginator.page(1)
    except EmptyPage:
        prod_page = paginator.page(paginator.num_pages)

    return render(request, 'store_products/product_list/list.html',{
        'categories': categories,
        'current_category': current_category,
        'brands': brands,
        'products': prod_page,
        'product_count': prod_count,
        'org': organization,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
    })
