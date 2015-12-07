import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist
from api.models.ec.subdomain import SubDomain
from ecantina_project.secret_settings import *


def http_403_page(request):
    org_id = 0
    store_id = 0
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_base/403.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def http_404_page(request):
    org_id = 0
    store_id = 0
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)
    
    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Display the view with all our model information.
    return render(request, 'store_base/403.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def storefront_redirect(request, name=""):
    """
        Function will lookup the domain name and redirect the user to
        the respected storefront at the particular sub-domain.
    """
    # Find the subdomain associated with this organization.
    try:
        this_subdomain = SubDomain.objects.get(name=name)
    except SubDomain.DoesNotExist:
        return HttpResponseRedirect("/404")
    
    url = SECRET_HTTP_PROTOCOL+this_subdomain.name+"."+SECRET_DOMAIN
    return HttpResponseRedirect(url)

# Note:
# http://www.djangobook.com/en/2.0/chapter03.html
