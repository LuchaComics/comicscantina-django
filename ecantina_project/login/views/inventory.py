import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inventory.forms.loginform import LoginForm
from inventory.models.ec.employee import Employee


def login_page(request):
    return render(request, 'login/inventory.html',{
        'form': LoginForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


def login_authentication(request):
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


def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'you are logged off'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def validate_user(user):
    if user is not None:
        if user.is_active:
            try:
                employee = Employee.objects.get(user=user)
                return {'status' : 'success', 'message' : 'logged on'}
            except Employee.DoesNotExist:
                return {'status' : 'failure', 'message' : 'you are not an employee'}
        else:
            return {'status' : 'failure', 'message' : 'you are suspended'}
    else:
        return {'status' : 'failure', 'message' : 'wrong username or password'}