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
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm
from inventory_setting.forms.organizationform import OrganizationForm
from inventory_setting.forms.storeform import StoreForm
from inventory_setting.forms.org_shipping_preference_form import OrgShippingPreferenceForm
from inventory_setting.forms.org_shipping_rates_form import OrgShippingRateForm


@login_required(login_url='/store/register/step1')
def step1_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)

    # If user is logged in, fetch the Customer record or create one.
    customer = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)

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
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # If user is logged in, fetch the Customer record or create one.
    customer = None
    this_org = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        this_org = Organization.objects.get(administrator__id=request.user.id)

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
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # Fetch the current session information we are working with.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    this_org = Organization.objects.get(administrator__id=request.user.id)
    try:
        this_store = Store.objects.get(organization__administrator__id=request.user.id)
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


@login_required(login_url='/store/register/step1')
def step4_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # Fetch the current session information we are working with.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    this_org = Organization.objects.get(administrator__id=request.user.id)
    try:
        this_store = Store.objects.get(organization__administrator__id=request.user.id)
    except Store.DoesNotExist:
        this_store = None

    # Get our organization preferences.
    try:
        org_preference = OrgShippingPreference.objects.get(organization=this_org)
    except OrgShippingPreference.DoesNotExist:
        org_preference = OrgShippingPreference.objects.create(
            organization_id = this_org.org_id,
        )
    
    # If we don't have the shipping rates set then add them in now, else we
    # just fetch the previously created rates.
    ca_rate = None
    us_rate = None
    mx_rate = None
    if len(org_preference.rates.all()) is 0:
        # Create for Canda, United States and Mexico
        canada = OrgShippingRate.objects.create(
            organization_id = this_org.org_id,
            country = 124,
        )
        org_preference.rates.add(canada)
        united_states = OrgShippingRate.objects.create(
            organization_id = this_org.org_id,
            country = 840,
        )
        org_preference.rates.add(united_states)
        mexico = OrgShippingRate.objects.create(
            organization_id = this_org.org_id,
            country = 484,
        )
        org_preference.rates.add(mexico)
    
        ca_rate = OrgShippingRate.objects.get(
            organization_id=this_org.org_id,
            country = 124,
        )
        us_rate = OrgShippingRate.objects.get(
            organization_id=this_org.org_id,
            country = 840,
        )
        mx_rate = OrgShippingRate.objects.get(
            organization_id=this_org.org_id,
            country = 484,
        )
    else:
        ca_rate = OrgShippingRate.objects.get(organization_id=this_org.org_id,country=124)
        us_rate = OrgShippingRate.objects.get(organization_id=this_org.org_id,country=840)
        mx_rate = OrgShippingRate.objects.get(organization_id=this_org.org_id,country=484)

    # Display the view with all our model information.
    return render(request, 'inventory_register/step4/view.html',{
        'org_form': OrgShippingPreferenceForm(instance=org_preference),
        'ca_form': OrgShippingRateForm(instance=ca_rate),
        'us_form': OrgShippingRateForm(instance=us_rate),
        'mx_form': OrgShippingRateForm(instance=mx_rate),
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


@login_required(login_url='/store/register/step1')
def step5_page(request, org_id=0, store_id=0):
    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(int(org_id))
    store = Store.objects.get_or_none(int(store_id))
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    
    # If user is logged in, fetch the Customer record or create one.
    customer = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)

    # Fetch the current session information we are working with.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    this_org = Organization.objects.get(administrator__id=request.user.id)
    try:
        this_store = Store.objects.get(organization__administrator__id=request.user.id)
    except Store.DoesNotExist:
        this_store = None

    # Display the view with all our model information.
    return render(request, 'inventory_register/step5/view.html',{
        'this_org': this_org,
        'this_store': this_store,
        'employee': employee,
        'customer': customer,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'register',
    })
