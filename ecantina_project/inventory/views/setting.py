import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.employee import Employee
from inventory.models.ec.store import Store
from inventory.forms.storeform import StoreForm
from inventory.forms.organizationform import OrganizationForm
from inventory.forms.imageuploadform import ImageUploadForm
from inventory.forms.userform import UserForm


# Organization
#-------------


@login_required(login_url='/inventory/login')
def org_settings_page(request, org_id, store_id):
    employee = Employee.objects.get(user=request.user)
    form = OrganizationForm(instance=employee.organization)
    logo = employee.organization.logo
    user_form = UserForm(instance=request.user)
    return render(request, 'inventory/setting/org/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'upload_id': 0 if logo is None else logo.upload_id,
        'tab':'org_settings',
        'employee': employee,
        'form': form,
        'user_form': user_form,
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


def ajax_org_save_logo(request, org_id, store_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch objects
            organization = Organization.objects.get(org_id=org_id)
            
            # Delete existing image if it exists.
            try:
                upload_id = request.POST['upload_id']
                if upload_id is not '':
                    logo = ImageUpload.objects.get(upload_id=int(upload_id))
                    logo.delete()
            except ImageUpload.DoesNotExist:
                pass

            # Save the new image.
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                
                # Update organization with new logo image.
                organization.logo = form.instance
                organization.save()
                
                # Return status.
                response_data = {
                    'status' : 'success',
                    'message' : 'saved',
                    'src': form.instance.image.url,
                    'id': form.instance.upload_id,
                }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_save_org_data(request, org_id, store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            organization = Organization.objects.get(org_id=org_id)
            
            # Save Organization
            form = OrganizationForm(request.POST, instance=organization)
            if form.is_valid():  # Ensure no missing fields are entered.
                # Include logo with saving.
                try:
                    upload_id = request.POST['upload_id']
                    if upload_id is not '':
                        organization.logo = ImageUpload.objects.get(upload_id=int(upload_id))
                except ImageUpload.DoesNotExist:
                    pass
                form.save()
            else:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : json.dumps(form.errors
                )}), content_type="application/json")

            # Save Administrator
            form = UserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : json.dumps(form.errors
                )}), content_type="application/json")

            # Success
            response_data = {'status' : 'success', 'message' : 'saved',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



# Stores
#-------------


@login_required(login_url='/inventory/login')
def edit_store_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    store = Store.objects.get(store_id=store_id)
    employee = Employee.objects.get(user=request.user)
    
    # Return all the stores belonging to this organization EXCEPT
    # the main store we are logged in as.
    stores =  Store.objects.filter(organization=organization)
    stores =  stores.filter(~Q(store_id = store_id))
        
    form = StoreForm(instance=store)
    logo = employee.organization.logo
    return render(request, 'inventory/setting/store/edit/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'this_store_id': this_store_id,
        'stores': stores,
        'upload_id': 0 if logo is None else logo.upload_id,
        'tab':'store_settings',
        'employee': employee,
        'form': form,
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/inventory/login')
def store_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    
    # Return all the stores belonging to this organization EXCEPT
    # the main store we are logged in as.
    stores =  Store.objects.filter(organization=organization)
    stores =  stores.filter(~Q(store_id = store_id))
    
    employee = Employee.objects.get(user=request.user)
    form = OrganizationForm(instance=employee.organization)
    logo = employee.organization.logo
    user_form = UserForm(instance=request.user)
    return render(request, 'inventory/setting/store/add/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'this_store_id': this_store_id,
        'stores': stores,
        'upload_id': 0 if logo is None else logo.upload_id,
        'tab':'store_settings',
        'employee': employee,
        'form': form,
        'user_form': user_form,
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
