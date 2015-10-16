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


def registration_step1_page(request):
    return render(request, 'register/store/step1.html',{
        'user_form': UserForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/store/register/step1')
def registration_step2_page(request):
    return render(request, 'register/store/step2.html',{
        'customer_form': CustomerForm(initial={'joined':datetime.now()}),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/store/register/step1')
def registration_step3_page(request):
    return render(request, 'register/store/step3.html',{
                  'customer_form': CustomerForm(initial={'joined':datetime.now()}),
                  'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
                  'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
                  'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })