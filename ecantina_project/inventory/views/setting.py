import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventory.forms.organizationform import OrganizationForm
from inventory.models.ec.employee import Employee


# Organization
#-------------

@login_required(login_url='/inventory/login')
def org_settings_page(request, org_id, store_id):
    employee = Employee.objects.get(user=request.user)
    form = OrganizationForm(instance=employee.organization)
    return render(request, 'inventory/setting/org.html',{
        'org_id': org_id,
        'store_id': store_id,
        'tab':'settings',
        'employee': employee,
        'form': form,
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


# Stores
#-------------


@login_required(login_url='/inventory/login')
def store_settings_page(request, org_id, store_id):
    return render(request, 'inventory/setting/store.html',{
        'org_id': org_id,
        'store_id': store_id,
        'tab':'settings',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
