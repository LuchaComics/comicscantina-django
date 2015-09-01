import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.tag import Tag
from api.models.ec.promotion import Promotion
from api.models.ec.product import Product


def list_page(request, org_id=0, cat_id=0):
    organization = Organization.objects.get(org_id=org_id)
    categories = Category.objects.all().order_by('category_id')
    try:
        current_category = Category.objects.get(category_id=cat_id)
    except:
        current_category = 'All Products'
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    promotions = Promotion.objects.all()

    products = Product.objects.filter(organization=org_id, category=cat_id)


    return render(request, 'store_products/product_list/list.html',{
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'organization' :organization,
        'categories' : categories,
        'current_category' : current_category,
        'brands' : brands,
        'tags' : tags,
        'promotions' : promotions,
        'products' : products,
    })
