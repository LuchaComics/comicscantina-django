import json
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product


@login_required(login_url='/inventory/login')
def orders_page(request, org_id, store_id):
    return render(request, 'inventory_order/master.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'orders',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/inventory/login')
def order_details_page(request, org_id, store_id, receipt_id):
    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None
    try:
        products = Product.objects.filter(receipt_id=receipt_id)
    except Product.DoesNotExist:
        products = None
    store = Store.objects.get(store_id=store_id)
    tax_rate = Decimal(store.tax_rate) * Decimal(100)
    return render(request, 'inventory_order/detail.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': store,
        'receipt': receipt,
        'products': products,
        'tax_rate': tax_rate,
        'tab':'orders',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })

