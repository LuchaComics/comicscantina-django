import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def authentication_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_customer/authentication/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'my_account',
    })


@login_required(login_url='/customer/authentication')
def my_account_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_customer/my_account/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'my_account',
    })


@login_required(login_url='/customer/authentication')
def order_history_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # Fetch required data.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Fetch Order List
    try:
        all_receipts = Receipt.objects.filter(customer=customer)
    except Receipt.DoesNotExist:
        all_receipts = None
    
    # Display the view with all our model information.
    return render(request, 'store_customer/order_history/master.html',{
        'all_receipts': all_receipts,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'order_history',
        'NEW_ORDER_STATUS': constants.NEW_ORDER_STATUS,
        'PICKED_STATUS': constants.PICKED_STATUS,
        'SHIPPED_STATUS': constants.SHIPPED_STATUS,
        'RECEIVED_STATUS': constants.RECEIVED_STATUS,
        'IN_STORE_SALE_STATUS': constants.IN_STORE_SALE_STATUS,
        'ONLINE_SALE_STATUS': constants.ONLINE_SALE_STATUS,
        'CASH_PAYMENT_METHOD': constants.CASH_PAYMENT_METHOD,
        'DEBIT_CARD_PAYMENT_METHOD': constants.DEBIT_CARD_PAYMENT_METHOD,
        'CREDIT_CARD_PAYMENT_METHOD': constants.CREDIT_CARD_PAYMENT_METHOD,
        'GIFT_CARD_PAYMENT_METHOD': constants.GIFT_CARD_PAYMENT_METHOD,
        'STORE_POINTS_PAYMENT_METHOD': constants.STORE_POINTS_PAYMENT_METHOD,
        'CHEQUE_PAYMENT_METHOD': constants.CHEQUE_PAYMENT_METHOD,
        'PAYPAL_PAYMENT_METHOD': constants.PAYPAL_PAYMENT_METHOD,
        'INVOICE_PAYMENT_METHOD': constants.INVOICE_PAYMENT_METHOD,
        'OTHER_PAYMENT_METHOD': constants.OTHER_PAYMENT_METHOD,
    })


@login_required(login_url='/customer/authentication')
def order_details_page(request, org_id=0, store_id=0, receipt_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    receipt_id = int(receipt_id)
    if receipt_id is 0:
        if org_id is not 0 and store_id is 0:
            receipt_id = org_id
        if org_id is not 0 and store_id is not 0:
            receipt_id = store_id

    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # Fetch required data.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Fetch Specific Order
    try:
        this_receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        this_receipt = None
    
    # Display the view with all our model information.
    return render(request, 'store_customer/order_history/detail.html',{
        'this_receipt': this_receipt,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'order_history',
        'NEW_ORDER_STATUS': constants.NEW_ORDER_STATUS,
        'PICKED_STATUS': constants.PICKED_STATUS,
        'SHIPPED_STATUS': constants.SHIPPED_STATUS,
        'RECEIVED_STATUS': constants.RECEIVED_STATUS,
        'IN_STORE_SALE_STATUS': constants.IN_STORE_SALE_STATUS,
        'ONLINE_SALE_STATUS': constants.ONLINE_SALE_STATUS,
        'CASH_PAYMENT_METHOD': constants.CASH_PAYMENT_METHOD,
        'DEBIT_CARD_PAYMENT_METHOD': constants.DEBIT_CARD_PAYMENT_METHOD,
        'CREDIT_CARD_PAYMENT_METHOD': constants.CREDIT_CARD_PAYMENT_METHOD,
        'GIFT_CARD_PAYMENT_METHOD': constants.GIFT_CARD_PAYMENT_METHOD,
        'STORE_POINTS_PAYMENT_METHOD': constants.STORE_POINTS_PAYMENT_METHOD,
        'CHEQUE_PAYMENT_METHOD': constants.CHEQUE_PAYMENT_METHOD,
        'PAYPAL_PAYMENT_METHOD': constants.PAYPAL_PAYMENT_METHOD,
        'INVOICE_PAYMENT_METHOD': constants.INVOICE_PAYMENT_METHOD,
        'OTHER_PAYMENT_METHOD': constants.OTHER_PAYMENT_METHOD,
    })


@login_required(login_url='/customer/authentication')
def wishlist_page(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_customer/wishlist/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'wishlist',
    })
