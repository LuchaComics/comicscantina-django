import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.section import Section
from inventory_setting.forms.userform import UserForm


@login_required(login_url='/inventory/login')
def admin_settings_page(request, org_id, store_id):
    employee = Employee.objects.get(user=request.user)
    return render(request, 'inventory_setting/admin/view.html',{
        'org': employee.organization,
        'store': Store.objects.get(store_id=store_id),
        'tab':'admin_settings',
        'employee': employee,
        'user_form': UserForm(instance=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def ajax_update_password(request):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            old_password = request.POST['old_password']
            password = request.POST['password']
            repeat_password = request.POST['password_repeated']
            
            # Validate password.
            if request.user.check_password(old_password) == False:
                response_data = {'status' : 'failure', 'message' : 'invalid old password' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password is '' or request is '':
                response_data = {'status' : 'failure', 'message' : 'blank passwords are not acceptable' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password != repeat_password:
                response_data = {'status' : 'failure', 'message' : 'passwords do not match' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Update model
            request.user.set_password(password)
            request.user.save()
    
        response_data = {'status' : 'success', 'message' : 'updated password'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")