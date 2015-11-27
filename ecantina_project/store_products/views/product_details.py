import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.gcd.story import GCDStory
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def details_page(request, product_id=0):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    organization = request.organization
    store = request.store
    product_id = int(product_id)
   
    # Redirect the user to a forbidden error if the store or organization
    # are not listed.
    if organization:
        if organization.is_listed is False:
            return HttpResponseRedirect("/403")
    if store:
        if store.is_listed is False:
            return HttpResponseRedirect("/403")

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)

    # Fetch objects used for searching criteria.
    try:
        categories = Category.objects.all().order_by('category_id')
    except Category.DoesNotExist:
        categories = None

    # Fetch the product details
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        product = None
    try:
        comic = Comic.objects.get(product__product_id=product_id)
    except Comic.DoesNotExist:
        comic = None

    # Fetch the Stories per comic
    try:
        stories = GCDStory.objects.filter(issue_id=comic.issue_id)
    except GCDStory.DoesNotExist:
        stories = None

    return render(request, 'store_products/product_details/details.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': organization,
        'store': store,
        'categories': categories,
        'comic': comic,
        'stories': stories,
        'product': product,
    })
