import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inventory_base.forms.loginform import LoginForm
from api.models.ec.employee import Employee
from api.models.ec.store import Store


def login_page(request):
    return render(request, 'login/inventory.html',{
        'form': LoginForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


def ajax_login_authentication(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            user = authenticate(
                username=request.POST.get('username').lower(),
                password=request.POST.get('password')
            )
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response_data = {'status': 'success', 'message': 'logged on', 'user_id': user.id }
                else:
                    response_data = {'status' : 'failure', 'message' : 'you are suspended'}
            else:
                response_data = {'status' : 'failure', 'message' : 'wrong username or password'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_logout_authentication(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
            response_data = {'status' : 'success', 'message' : 'you are logged off'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
