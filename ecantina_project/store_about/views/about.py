import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from api.models.ec.organization import Organization
from api.models.ec.store import Store

def about_page(request, org_id):
    organization = Organization.objects.get(org_id=org_id)

    return render(request, 'store_about/main/about.html',{
        'org' : organization,
        'stores' : Store.objects.filter(organization=organization),
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
    })
