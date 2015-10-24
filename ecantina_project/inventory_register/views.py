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
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm


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

    # Display the view with all our model information.
    return render(request, 'inventory_register/step1/view.html',{
        'employee': employee,
        'org': org,
        'store': store,
        'local_css_library' : settings.STORE_CSS_LIBRARY,
        'local_js_library_header' : settings.STORE_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.STORE_JS_LIBRARY_BODY,
        'page' : 'register',
    })
