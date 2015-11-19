import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ecantina_project import constants
from register.forms import StoreRegistrationForm
from inventory_base.forms.imageuploadform import ImageUploadForm
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm


def registration_step1_page(request, org_id=0, store_id=0,):
    # Fetch the Organization / Store.
    try:
        org = Organization.objects.get(org_id=int(org_id))
    except Organization.DoesNotExist:
        org = None
    try:
        store = Store.objects.get(store_id=int(store_id))
    except Store.DoesNotExist:
        store = None
    
    return render(request, 'register/store/step1.html',{
        'org': org,
        'store': store,
        'user_form': UserForm(),
    })


@login_required(login_url='/store/register/step1')
def registration_step2_page(request, org_id=0, store_id=0,):
    # Fetch the Organization / Store.
    try:
        org = Organization.objects.get(org_id=int(org_id))
    except Organization.DoesNotExist:
        org = None
    try:
        store = Store.objects.get(store_id=int(store_id))
    except Store.DoesNotExist:
        store = None
    
    return render(request, 'register/store/step2.html',{
        'org': org,
        'store': store,
        'customer_form': CustomerForm(initial={'joined':datetime.now()}),
    })


@login_required(login_url='/store/register/step1')
def registration_step3_page(request, org_id=0, store_id=0,):
    # Fetch the Organization / Store.
    try:
        org = Organization.objects.get(org_id=int(org_id))
    except Organization.DoesNotExist:
        org = None
    try:
        store = Store.objects.get(store_id=int(store_id))
    except Store.DoesNotExist:
        store = None
    
    return render(request, 'register/store/step3.html',{
        'org': org,
        'store': store,
        'customer_form': CustomerForm(initial={'joined':datetime.now()}),
    })