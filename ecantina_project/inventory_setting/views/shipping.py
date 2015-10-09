import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from inventory_setting.forms.org_shipping_preference_form import OrgShippingPreferenceForm
from inventory_setting.forms.org_shipping_rates_form import OrgShippingRateForm


@login_required(login_url='/inventory/login')
def shipping_settings_page(request, org_id, store_id):
    # Get our organization preferences.
    try:
        org_preference = OrgShippingPreference.objects.get(organization_id=org_id)
    except OrgShippingPreference.DoesNotExist:
        org_preference = OrgShippingPreference.objects.create(
            organization_id = org_id,
        )

    # If we don't have the shipping rates set then add them in now.
    if len(org_preference.rates.all()) is 0:
        # Create for Canda, United States and Mexico
        canada = OrgShippingRate.objects.create(
            organization_id = org_id,
            country = 124,
        )
        org_preference.rates.add(canada)
        united_states = OrgShippingRate.objects.create(
            organization_id = org_id,
            country = 840,
        )
        org_preference.rates.add(united_states)
        mexico = OrgShippingRate.objects.create(
            organization_id = org_id,
            country = 484,
        )
        org_preference.rates.add(mexico)

    ca_rate = OrgShippingRate.objects.get(
        organization_id=org_id,
        country = 124,
    )
    us_rate = OrgShippingRate.objects.get(
        organization_id=org_id,
        country = 840,
    )
    mx_rate = OrgShippingRate.objects.get(
        organization_id=org_id,
        country = 484,
    )

    return render(request, 'inventory_setting/shipping/master.html',{
        'org_form': OrgShippingPreferenceForm(instance=org_preference),
        'ca_form': OrgShippingRateForm(instance=ca_rate),
        'us_form': OrgShippingRateForm(instance=us_rate),
        'mx_form': OrgShippingRateForm(instance=mx_rate),
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'employee': Employee.objects.get(user=request.user),
        'tab':'shipping_settings',
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })

@login_required(login_url='/inventory/login')
def shipping_details_settings_page(request, org_id, store_id, country_id):
    rate = OrgShippingRate.objects.get(
        organization_id=org_id,
        country = int(country_id),
    )
    
    return render(request, 'inventory_setting/shipping/details.html',{
        'form': OrgShippingRateForm(instance=rate),
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'employee': Employee.objects.get(user=request.user),
        'tab':'shipping_settings',
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })