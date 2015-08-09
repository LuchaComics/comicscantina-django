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
from api.models.ec.cart import Cart


@login_required(login_url='/inventory/login')
def checkout_page(request, org_id, store_id, cart_id):
    return render(request, 'inventory_checkout/item/index.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'cart': Cart.objects.get(cart_id=cart_id),
        'tab':'checkout',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })

@login_required(login_url='/inventory/login')
def content_page(request, org_id, store_id, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    sub_total_amount = 0.0
    total_amount = 0.0
    total_tax = 0.0
    
    for product in cart.products.all():
        sub_total_amount += product.price
        if cart.has_tax:
           total_tax += 0.13 * product.price
    total_amount = sub_total_amount + total_tax
            
    return render(request, 'inventory_checkout/item/content.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'cart': cart,
        'sub_total_amount': sub_total_amount,
        'total_tax': total_tax,
        'total_amount': total_amount,
        'employee': Employee.objects.get(user=request.user),
    })