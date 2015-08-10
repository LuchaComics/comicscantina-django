import json
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.product import Product
from api.models.ec.receipt import Receipt


@login_required(login_url='/inventory/login')
def checkout_page(request, org_id, store_id, receipt_id):
    return render(request, 'inventory_checkout/item/index.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'receipt': Receipt.objects.get(receipt_id=receipt_id),
        'tab':'checkout',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/inventory/login')
def content_page(request, org_id, store_id, receipt_id):
    # Note: If you want to know how to handle decimal places and rounding
    #       then checkout this URL:
    #       https://docs.python.org/3/library/decimal.html#decimal-faq
    
    store = Store.objects.get(store_id=store_id)
    receipt = Receipt.objects.get(receipt_id=receipt_id)
    sub_total_amount = Decimal(0.00)
    total_amount = Decimal(0.00)
    total_tax = Decimal(0.00)
    
    for product in receipt.products.all():
        sub_total_amount += Decimal(product.price)
        if receipt.has_tax:
           total_tax += Decimal(store.tax_rate) * Decimal(product.price)
    total_amount = Decimal(sub_total_amount) + Decimal(total_tax)

    TWOPLACES = Decimal(10) ** -2       # same as Decimal('0.01')
    return render(request, 'inventory_checkout/item/content.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'receipt': receipt,
        'sub_total_amount': sub_total_amount.quantize(TWOPLACES),
        'tax': Decimal(store.tax_rate) * Decimal(100.00),
        'total_tax': total_tax.quantize(TWOPLACES),
        'total_amount': total_amount.quantize(TWOPLACES),
        'employee': Employee.objects.get(user=request.user),
    })


def ajax_change_discount_type(request, org_id, store_id, receipt_id, product_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                product = Product.objects.get(product_id=int(product_id))
                
                # Reset amounts.
                product.discount = 0.00
                product.price = product.sub_price
                
                # Switch discount type
                if product.discount_type is 1: # Percent
                    product.discount_type = 2
                elif product.discount_type is 2: # Amount
                    product.discount_type = 1
                
                # Save changes and return success.
                product.save()
                response_data = {'status': 'success','message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_change_discount_amount(request, org_id, store_id, receipt_id, product_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                product = Product.objects.get(product_id=int(product_id))
                discount = request.POST['discount']
                if product.discount_type is 1: # Percent
                    product.discount = discount
                    rate = Decimal(discount) / Decimal(100)
                    discount = Decimal(rate) * Decimal(product.sub_price)
                elif product.discount_type is 2: # Amount
                    product.discount = discount
                product.price = Decimal(product.sub_price) - Decimal(discount)
                product.save()
                response_data = {'status': 'success', 'message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_change_tax(request, org_id, store_id, receipt_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                receipt = Receipt.objects.get(receipt_id=int(receipt_id))
                receipt.has_tax = not receipt.has_tax
                receipt.save()
                response_data = {'status': 'success', 'message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_verify(request, org_id, store_id, receipt_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                receipt = Receipt.objects.get(receipt_id=int(receipt_id))
                for product in receipt.products.all():
                    if product.is_sold is True:
                        return HttpResponse(json.dumps({
                            'status': 'failed',
                            'message': str(product.product_id),
                        }), content_type="application/json")
                response_data = {'status': 'success', 'message': 'verified',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_process_receipt(request, org_id, store_id, receipt_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                receipt = Receipt.objects.get(receipt_id=int(receipt_id))
                
                # Iterate through all the products and make sure they are all
                # set for "is_sold" to be true thus indicating no other receipt
                # can access this product.
                for product in receipt.products.all():
                    product.is_sold = True
                    product.save()

                # Iterate through all the products and create a calculate
                # our totals.
                sub_tota_amount = Decimal(0.00)
                total_discount_amount = Decimal(0.00)
                total_tax_amount = Decimal(0.00)
                total_amount = Decimal(0.00)
                for product in receipt.products.all():
                    # Process discount
                    if product.discount_type is 1: # Percent
                        rate = Decimal(product.discount) / Decimal(100)
                        discount_amount = Decimal(rate) * Decimal(product.sub_price)
                    elif product.discount_type is 2: # Amount
                        discount_amount =  product.discount
                    post_discount_price = product.sub_price - discount_amount
                    total_discount_amount += discount_amount
                    
                    # Process sub-amount
                    sub_tota_amount += post_discount_price
                    
                    # Process tax
                    if receipt.has_tax:
                        tax_rate = Decimal(0.13)
                        tax_amount = post_discount_price * tax_rate
                    total_tax_amount += tax_amount
                
                    # Process total amount
                    total_amount += post_discount_price + tax_amount

                # Update receipt
                receipt.sub_total = sub_tota_amount
                receipt.discount_amount = total_discount_amount
                receipt.tax_amount = total_tax_amount
                receipt.total_amount = total_amount
                
                # Finally, tell the receipt that it is closed to prevent further
                # accessing of this receipt and then save.
                receipt.has_finished = True
                receipt.has_paid = True
                receipt.save()
                response_data = {'status': 'success', 'message': 'processed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
