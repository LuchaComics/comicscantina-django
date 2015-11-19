import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inventory_base.forms.loginform import LoginForm
from api.models.ec.employee import Employee
from api.models.ec.store import Store


def login_page(request):
    # If the user is already authenticated then simply redirect to the latest
    # dashboard page, else load the login page.
    if request.user.is_authenticated():
        employee = Employee.objects.get(user__id=request.user.id)
        store = Store.objects.filter(organization=employee.organization)[0]
        dashboard_url = "/inventory/"+str(employee.organization_id)
        dashboard_url += "/"+str(store.store_id)+"/"+"dashboard"
        return HttpResponseRedirect(dashboard_url)
    else:
        return render(request, 'login/inventory.html',{
            'form': LoginForm(),
        })


def ajax_login_authentication(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            user = authenticate(
                username=request.POST.get('username').lower(),
                password=request.POST.get('password')
            )
            # Perform a battery of tests on the user account to ensure
            # it meets the requirements for logging into our system.
            response_data = validate_user(user)
            
            # If user meets requirements then offically login the user.
            if response_data['status'] == 'success':
                login(request, user)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_logout_authentication(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
            response_data = {'status' : 'success', 'message' : 'you are logged off'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def validate_user(user):
    if user is not None:
        if user.is_active:
            try:
                # Get the employee and return the first store in the organization.
                employee = Employee.objects.get(user=user)
                store = Store.objects.filter(organization=employee.organization)[0]
                return {
                    'status': 'success',
                    'message': 'logged on',
                    'org_id': employee.organization.org_id,
                    'store_id': store.store_id,
                }
            except Employee.DoesNotExist:
                return {'status' : 'failure', 'message' : 'you are not an employee'}
        else:
            return {'status' : 'failure', 'message' : 'you are suspended'}
    else:
        return {'status' : 'failure', 'message' : 'wrong username or password'}