import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from api.models.ec.comic import Comic


def front_page(request, org_id=0):
    try:
        featured_comics = Comic.objects.filter(
            product__is_available=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_featured=True,
        )
    except Comic.DoesNotExist:
        featured_comics = None
    print(featured_comics)
    try:
        new_comics = Comic.objects.filter(
            product__is_available=True,
            product__store__is_aggregated=True,
            product__is_sold=False,
            product__is_new=True,
        )
    except Comic.DoesNotExist:
        new_comics = None


    return render(request, 'store_landpage/index.html',{
        'featured_comics': featured_comics,
        'new_comics': new_comics,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'home',
    })
