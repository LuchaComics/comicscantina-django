import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.product import Product

def details_page(request, org_id=0, store_id=0, prod_id=0):
    try:
        product = Product.objects.get(organization=org_id, product_id=prod_id)
    except Product.DoesNotExist:
        product = None

    return render(request, 'store_products/product_details/details.html',{
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'product' : product,
    })
