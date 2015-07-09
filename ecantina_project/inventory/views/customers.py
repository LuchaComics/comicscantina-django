import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventory.models.ec.organization import Organization
from inventory.models.ec.employee import Employee
from inventory.models.ec.store import Store
from inventory.forms.customerform import CustomerForm


@login_required(login_url='/inventory/login')
def customers_page(request, org_id, store_id):
    return render(request, 'inventory/customers/list/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def ajax_refresh_table(request, org_id, store_id):
    return render(request, 'inventory/customers/list/table.html',{
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
    return render(request, 'inventory/customers/add/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': CustomerForm(initial={'joined':datetime.now()}),
        'tab':'add_customer',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def ajax_add_customer(request, org_id, store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid() is False:
                response_data = {
                    'status': 'failed',
                    'message' : json.dumps(form.errors),
                }
            else:
                form.save()  # Save our customer object.
                
                # Add it to the organization.
                try:
                    org = Organization.objects.get(org_id=org_id)
                    org.customers.add(form.instance)
                    org.save()
                except:
                    pass

                response_data = {
                    'status': 'success',
                    'message': 'saved',
                    'customer_id': form.instance.customer_id,
                }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

