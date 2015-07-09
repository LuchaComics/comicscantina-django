import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventory.models.ec.organization import Organization
from inventory.models.ec.employee import Employee
from inventory.models.ec.store import Store


@login_required(login_url='/inventory/login')
def customers_page(request, org_id, store_id):
    return render(request, 'inventory/customers/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/inventory/login')
def add_customer_page(request, org_id, store_id):
    return render(request, 'inventory/customers/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'add_customer',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
