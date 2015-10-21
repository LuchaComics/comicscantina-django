import json
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, payment_was_flagged
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from inventory_base.forms.customerform import CustomerForm


def cart_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/cart/view.html',{
        'receipt': receipt,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'home',
    })


@login_required(login_url='/')
def checkout_shipping_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_billing_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/billing/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_shipping_method_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Lock out 'Shipping' option if a single product in the cart requires
    # in store pickup only.
    has_no_shipping = False
    for product in receipt.products.all():
        if product.has_no_shipping:
            has_no_shipping = True

    # Lock out 'Shipping' option if the organization does not support it.
    preference = OrgShippingPreference.objects.get_by_org_or_none(organization=org)
    if preference is not None:
        if preference.is_pickup_only:
            has_no_shipping = True

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping_method/view.html',{
        'has_no_shipping': has_no_shipping,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_payment_method_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/payment_method/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@csrf_exempt
@login_required(login_url='/')
def checkout_thank_you_page(request, param1_id=0, param2_id=0, param3_id=0):
    # Adaptive URL parameter extractor.
    param1_id = int(param1_id)
    param2_id = int(param2_id)
    param3_id = int(param3_id)
    org_id = 0
    store_id = 0
    receipt_id = 0
    if param1_id > 0 and param2_id == 0 and param3_id == 0:
        receipt_id = param1_id
    elif param1_id > 0 and param2_id > 0 and param3_id == 0:
        receipt_id = param2_id
        org_id = param1_id
    elif param1_id > 0 and param2_id > 0 and param3_id > 0:
        receipt_id = param3_id
        org_id = param1_id
        store_id = param2_id
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))

    # Fetch OLD receipt
    old_receipt = Receipt.objects.get_or_none(receipt_id=receipt_id)
    old_receipt.has_finished = True
    old_receipt.save()

    # Fetch Customer / Receipt
    # Note: Because our previous Receipt was set "has_finished" to true
    #       this will force a new cart to be opened / created here.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/thank_you/view.html',{
        'old_receipt': old_receipt,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@csrf_exempt
@login_required(login_url='/')
def checkout_cancel_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/cancel/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library': settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_order_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Generate our URLs & pick the payment email
    paypal_email = settings.PAYPAL_RECEIVER_EMAIL
    base_url = settings.SITE_DOMAIN_URL
    if org is not None and store is None:
        base_url += "/"+str(org.org_id)
        paypal_email = org.paypal_email
    if org is not None and store is not None:
        base_url += "/"+str(org.org_id)+"/"+str(store.store_id)
        paypal_email = store.paypal_email
    return_url = base_url+"/checkout/thank_you"
    cancel_url = base_url+"/checkout/cancel"

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user(request.user)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    
    # What you want the button to do.
    paypal_dict = {
        "business": paypal_email,
        "amount": str(receipt.total_amount),
        "item_name": "Comic Book(s) Purchase, Receipt #"+str(receipt.receipt_id),
        "invoice": str(receipt.receipt_id),
        "notify_url": "/checkout/" + reverse('paypal-ipn'),
        "return_url": return_url+"/"+str(receipt.receipt_id),
        "cancel_return": cancel_url,
        "custom": "perform_receipt_checkout",  # Custom command to correlate to some function later (optional)
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    # Display the view with all our model information.
    return render(request, 'store_checkout/order/view.html',{
        'paypal_form': form,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header': settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body': settings.STORE_JS_LIBRARY_BODY,
        'page': 'home',
    })
