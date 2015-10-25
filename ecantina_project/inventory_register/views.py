import json
from datetime import datetime
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.section import Section
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm
from inventory_setting.forms.organizationform import OrganizationForm
from inventory_setting.forms.storeform import StoreForm

@login_required(login_url='/store/register/step1')
def step1_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Detect if the employee already exists by finding an employee record
    # associated with this user account.
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    # If user is logged in, fetch the Customer record or create one.
    customer = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)

    # Display the view with all our model information.
    return render(request, 'inventory_register/step1/view.html',{
        'employee': employee,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'register',
    })


@login_required(login_url='/store/register/step1')
def step2_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Detect if the employee already exists by finding an employee record
    # associated with this user account.
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None
    
    # If user is logged in, fetch the Customer record or create one.
    customer = None
    this_org = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        this_org = Organization.objects.get(administrator=request.user)

    # Display the view with all our model information.
    return render(request, 'inventory_register/step2/view.html',{
        'form': OrganizationForm(instance=this_org),
        'employee': employee,
        'customer': customer,
        'org': org,
        'this_org': this_org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'register',
    })


@login_required(login_url='/store/register/step1')
def step3_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    
    # Detect if the employee already exists by finding an employee record
    # associated with this user account.
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None
    
    # If user is logged in, fetch the Customer record or create one.
    customer = None
    this_org = None
    this_store = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user(request.user)
        this_org = Organization.objects.get(administrator=request.user)
        try:
            this_store = Store.objects.get(organization__administrator=request.user)
        except Store.DoesNotExist:
            this_store = None
    
    # Display the view with all our model information.
    return render(request, 'inventory_register/step3/view.html',{
        'form': StoreForm(instance=this_store),
        'employee': employee,
        'customer': customer,
        'org': org,
        'this_org': this_org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'register',
    })
