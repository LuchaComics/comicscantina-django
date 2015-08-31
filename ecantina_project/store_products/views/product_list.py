import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings


def list_page(request, org_id=0):
    return render(request, 'store_products/product_list/list.html',{
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
    })
