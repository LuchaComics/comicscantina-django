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
from inventory.models.ec.section import Section
from inventory.forms.storeform import StoreForm
from inventory.forms.organizationform import OrganizationForm
from inventory.forms.imageuploadform import ImageUploadForm
from inventory.forms.userform import UserForm
from inventory.forms.sectionform import SectionForm
from inventory.forms.employeeform import EmployeeForm


# Stores - Common
#-----------------


@login_required(login_url='/inventory/login')
def ajax_refresh_sections(request, org_id, store_id, this_store_id):
    store = Store.objects.get(store_id=store_id)
    sections = Section.objects.filter(store=store)
    return render(request, 'inventory/setting/store/sections.html',{
        'sections': sections,
    })


@login_required()
def ajax_section(request, org_id, store_id, this_store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            organization = Organization.objects.get(org_id=org_id)
            store = Store.objects.get(store_id=this_store_id)
            section_id = request.POST['section_id']
            try:
                section = Section.objects.get(section_id=section_id)
            except Section.DoesNotExist:
                section = None
            form = SectionForm(request.POST, instance=section)
            form.instance.organization = organization
            form.instance.store = store
            if form.is_valid():  # Ensure no missing fields are entered.
                form.save()
                response_data = {'status' : 'success', 'message' : 'saved',}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_delete_section(request, org_id, store_id, this_store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            organization = Organization.objects.get(org_id=org_id)
            store = Store.objects.get(store_id=this_store_id)
            section_id = request.POST['section_id']
            try:
                Section.objects.get(section_id=section_id).delete()
                response_data = {'status' : 'success', 'message' : 'deleted',}
            except Section.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_save_store_data(request, org_id, store_id, this_store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                store = Store.objects.get(store_id=this_store_id)
            except Store.DoesNotExist:
                store = None
            form = StoreForm(request.POST, instance=store)
            form.instance.organization = Organization.objects.get(org_id=org_id)

            if form.is_valid():  # Ensure no missing fields are entered.
                # Include logo with saving.
                try:
                    upload_id = request.POST['upload_id']
                    if upload_id is not '':
                        form.logo = ImageUpload.objects.get(upload_id=int(upload_id))
                except ImageUpload.DoesNotExist:
                    pass
                form.save()
                response_data = {
                    'status': 'success',
                    'message': 'saved',
                    'store_id': form.instance.store_id,
                }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_save_store_logo(request, org_id, store_id, this_store_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
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
                
                # Update store with new logo image.
                try:
                    store = Store.objects.get(store_id=this_store_id)
                    store.logo = form.instance
                    store.save()
                    form.instance.is_assigned = True
                    form.save()
                except Store.DoesNotExist:
                    pass
                
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


# Stores - Edit
#---------------


@login_required(login_url='/inventory/login')
def edit_store_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    this_store = Store.objects.get(store_id=this_store_id)
    
    # Return all the stores belonging to this organization EXCEPT
    # the main store we are logged in as.
    stores =  Store.objects.filter(organization=organization)
    stores =  stores.filter(~Q(store_id = this_store_id))
    return render(request, 'inventory/setting/store/edit/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': this_store,
        'stores': stores,
        'sections': Section.objects.filter(store=this_store),
        'tab':'store_settings',
        'employee': Employee.objects.get(user=request.user),
        'form': StoreForm(instance=this_store),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


# Stores - Add
#--------------


@login_required(login_url='/inventory/login')
def store_settings_page(request, org_id, store_id):
    organization = Organization.objects.get(org_id=org_id)
    store = Store.objects.get(store_id=store_id)
    return render(request, 'inventory/setting/store/add/view.html',{
        'org': organization,
        'store': store,
        'stores': Store.objects.filter(organization=organization),
        'sections': Section.objects.filter(store=store),
        'tab':'store_settings',
        'employee': Employee.objects.get(user=request.user),
        'form': StoreForm(),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
