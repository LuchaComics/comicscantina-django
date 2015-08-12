import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store


@login_required(login_url='/inventory/login')
def pos_record_page(request, org_id, store_id):
    return render(request, 'inventory_checkout/record/index.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'checkout_record',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })