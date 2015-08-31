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


def list_page(request, org_id=0):
    organization = Organization.objects.get(org_id=org_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    promotions = Promotion.objects.all()


    return render(request, 'store_products/product_list/list.html',{
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'organization' :organization,
        'categories' : categories,
        'brands' : brands,
        'tags' : tags,
        'promotions' : promotions,
    })
