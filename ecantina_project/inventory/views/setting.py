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


# Organization - Edit
#---------------------


@login_required(login_url='/inventory/login')
def org_settings_page(request, org_id, store_id):
    employee = Employee.objects.get(user=request.user)
    form = OrganizationForm(instance=employee.organization)
    logo = employee.organization.logo
    return render(request, 'inventory/setting/org/view.html',{
        'org': employee.organization,
        'store': Store.objects.get(store_id=store_id),
        'upload_id': 0 if logo is None else logo.upload_id,
        'tab':'org_settings',
        'employee': employee,
        'form': form,
        'user_form': UserForm(instance=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


# Organization - Common
#-----------------------


@login_required()
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


@login_required()
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
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
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
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })



# User - Listing
#----------------


@login_required(login_url='/inventory/login')
def users_list_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    
    # Try to find the store we will be processing and their respected employees.
    try:
        this_store = Store.objects.get(store_id=this_store_id)
        employees = this_store.employees.all()
    except Store.DoesNotExist:
        this_store = None
        employees = Employee.objects.filter(organization=organization)

    return render(request, 'inventory/setting/users/list/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': this_store,
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user=request.user),
        'employees': employees,
        'form': StoreForm(),
        'tab':'users_settings',
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


# User - Common
#----------------

@login_required()
def ajax_save_employee_image(request, org_id, store_id, this_store_id, this_employee_id):
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
                
                # Update employee with new profile image.
                try:
                    employee = Employee.objects.get(employee_id=this_employee_id)
                    employee.profile = form.instance
                    employee.save()
                except Employee.DoesNotExist:
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


@login_required()
def ajax_save_user_data(request, org_id, store_id, this_store_id, this_employee_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            # Load up our employee & user objects.
            try:
                employee = Employee.objects.get(employee_id=this_employee_id)
                user = employee.user
            except Employee.DoesNotExist:
                employee = None
                user = None

            # Validate
            user_form = UserForm(request.POST, instance=user)
            employee_form = EmployeeForm(request.POST, instance=employee)
            employee_form.instance.organization = Organization.objects.get(org_id=org_id)
            if user_form.is_valid() is False:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : json.dumps(user_form.errors
                )}), content_type="application/json")
            if employee_form.is_valid() is False:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : json.dumps(employee_form.errors
                )}), content_type="application/json")
            
            # (If not initialized) create user, else update user.
            if user is None:
                email = user_form['email'].value().lower()
                user = User.objects.create_user(
                    email,  # Username
                    email,  # Email
                    user_form['password'].value(),
                )
                user.first_name = user_form['first_name'].value()
                user.last_name = user_form['last_name'].value()
                user.is_active = False;  # Need email verification to change status.
                user.save()
            else:
                user.username = user_form['email'].value().lower()
                user.email = user_form['email'].value().lower()
                user.first_name = user_form['first_name'].value()
                user.last_name = user_form['last_name'].value()
                password = user_form['password'].value()
                if password is not '':
                    pass
            
            # Fetch Profile Image. Update the user inside the profile image.
            try:
                upload_id = request.POST['upload_id']
                upload = None
                if upload_id is not '':
                    upload = ImageUpload.objects.get(upload_id=int(upload_id))
                    upload.user = user
                    upload.save()
                    employee_form.instance.profile = upload
            except ImageUpload.DoesNotExist:
                pass

            # Save Employee & return success message.
            employee_form.instance.user = user
            employee_form.save()
            response_data = {
                'status': 'success',
                'message': 'saved',
                'employee_id': employee_form.instance.employee_id,
            }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_delete_user(request, org_id, store_id, this_employee_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            # Load up our employee & user objects.
            try:
                employee = Employee.objects.get(employee_id=this_employee_id)
                user = employee.user
                images = ImageUpload.objects.filter(user=employee.user)
            except Employee.DoesNotExist:
                employee = None
                user = None
                images = None
        
            # Delete & return success
            for image in images:
                image.delete()
            user.delete()
            employee.delete()
            response_data = {
                'status': 'success',
                'message': 'deleted',
            }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_assign_employee_to_store(request, org_id, store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            this_employee_id = request.POST['this_employee_id']
            this_store_id = request.POST['this_store_id']
            
            # Find store & employee
            try:
                store = Store.objects.get(store_id=this_store_id)
            except Store.DoesNotExist:
                store = None
            try:
                employee = Employee.objects.get(employee_id=this_employee_id)
            except Employee.DoesNotExist:
                employee = None
        
            if employee is not None and store is not None:
                # Assignment - If employee exists for this store then remove it,
                # else then add it in there.
                if employee in store.employees.all():
                    store.employees.remove(employee)
                else:
                    store.employees.add(employee)
                response_data = {'status': 'success', 'message': 'saved',}
            else:
                response_data = {'status': 'failed', 'message': 'missing objects',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# User - Edit
#----------------


@login_required(login_url='/inventory/login')
def edit_user_settings_page(request, org_id, store_id, this_store_id, this_employee_id):
    # Try to find the user.
    try:
        this_employee = Employee.objects.get(employee_id=this_employee_id)
    except Employee.DoesNotExist:
        this_employee = None
    
    # Try to find the store we will be processing.
    try:
        this_store = Store.objects.get(store_id=this_store_id)
    except Store.DoesNotExist:
        this_store = None

    organization = Organization.objects.get(org_id=org_id)
    return render(request, 'inventory/setting/users/edit/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': this_store,
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user=request.user),
        'this_employee': this_employee,
        'form': EmployeeForm(instance=this_employee),
        'user_form': UserForm() if this_employee is None else UserForm(instance=this_employee.user),
        'tab':'users_settings',
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


# User - Add
#----------------


@login_required(login_url='/inventory/login')
def add_user_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    return render(request, 'inventory/setting/users/add/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': None,
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user=request.user),
        'this_employee': None,
        'employee_form': EmployeeForm(initial={'joined':datetime.now()}),
        'user_form': UserForm(),
        'tab':'users_settings',
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })