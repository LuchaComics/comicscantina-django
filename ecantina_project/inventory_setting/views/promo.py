import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.section import Section


@login_required(login_url='/inventory/login')
def promo_settings_page(request, org_id, store_id):
    organization = Organization.objects.get(org_id=org_id)
    
    return render(request, 'inventory_setting/promo/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': None,
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user=request.user),
        'tab':'promotion_settings',
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })