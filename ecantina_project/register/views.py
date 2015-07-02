import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from register.forms import StoreRegistrationForm
from inventory.forms.imageuploadform import ImageUploadForm
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee


def store_registration_page(request):
    return render(request, 'register/store.html',{
        'form': StoreRegistrationForm(),
        'image_form': ImageUploadForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


def ajax_store_save_image(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                response_data = {
                    'status' : 'success',
                    'message' : 'saved',
                    'src': form.instance.image.url,
                    'id': form.instance.upload_id,
            }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_create_account(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            form = StoreRegistrationForm(request.POST, request.FILES)
            if form.is_valid():  # Ensure no missing fields are entered.
                response_data = create(request, form)  # Create our store
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create(request, form):
    """
        Function creates the store in the inventory and returns the status.
    """
    # Create administrator
    response_data = create_user(form)
    if response_data['status'] is 'failure':
        return response_data

    # Create organization
    response_data = create_organization(form)
    if response_data['status'] is 'failure':
        return response_data

    # Create store
    response_data = create_store(form)
    if response_data['status'] is 'failure':
        return response_data

    # Create Owner Employee
    response_data = create_employee(form)
    if response_data['status'] is 'failure':
        return response_data

    return {
        'status' : 'success',
        'message' : 'successfully registered',
    }


def create_user(form):
    # Create the user in our database
    email = form['email'].value().lower()
    try:
        user = User.objects.create_user(
            email,  # Username
            email,  # Email
            form['password'].value(),
        )
        user.first_name = form['first_name'].value()
        user.last_name = form['last_name'].value()
        user.is_active = False;  # Need email verification to change status.
        user.save()
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering user.'
        }

    # Save reference to user for image.
    upload_id = form['hidden_upload_id'].value()
    if upload_id is not None and upload_id is not '':
        try:
            image_upload = ImageUpload.objects.get(upload_id=int(upload_id))
            image_upload.user = user
            image_upload.save()
        except ImageUpload.DoesNotExist:
            pass

    # Return success status
    return {
        'status' : 'success',
        'message' : 'user registered'
    }


def create_organization(form):
    # Get administrator
    email = form['email'].value().lower()
    administrator = User.objects.get(email=email)
    
    # Get Image
    upload_id = form['hidden_upload_id'].value()
    if upload_id is not None and upload_id is not '':
        try:
            image_upload = ImageUpload.objects.get(upload_id=int(upload_id))
        except ImageUpload.DoesNotExist:
            image_upload = None

    # Create organization
    try:
        Organization.objects.create(
            name=form['org_name'].value(),
            description = '',
            joined = datetime.now(),
            street_name=form['street_name'].value(),
            street_number=form['street_number'].value(),
            unit_number=form['unit_number'].value(),
            city=form['city'].value(),
            province=form['province'].value(),
            country=form['country'].value(),
            postal=form['postal'].value(),
            website = form['website'].value(),
            email = email,
            phone = form['phone'].value(),
            fax = form['fax'].value(),
            twitter_url = form['twitter'].value(),
            facebook_url = form['facebook'].value(),
            instagram_url = '',
            linkedin_url = '',
            github_url = '',
            google_url = '',
            youtube_url = '',
            flickr_url = '',
            administrator = administrator,
            logo = image_upload,
        )
        return {'status' : 'success', 'message' : 'user registered'}
    except:
        return {
            'status' : 'failure',
            'message' : 'an unknown error occured when creating organization'
        }


def create_store(form):
    # Get org
    org_name = form['org_name'].value()
    organization = Organization.objects.get(name=org_name)

    # Save Store
    try:
        store = Store.objects.create(
            organization=organization,
            name = 'Main Store',
            description = 'The main location.',
            joined = datetime.now(),
            street_name = form['street_name'].value(),
            street_number = form['street_number'].value(),
            unit_number = form['unit_number'].value(),
            city = form['city'].value(),
            province = form['province'].value(),
            country = form['country'].value(),
            postal = form['postal'].value(),
            website = form['website'].value(),
            email = form['email'].value().lower(),
            phone = form['phone'].value(),
            fax = form['fax'].value(),
        )
        return {'status' : 'success', 'message' : 'store registered'}
    except:
        return {
            'status' : 'failure',
            'message' : 'an unknown error occured when creating store'
        }


def create_employee(form):
    # Create the user in our database
    email = form['email'].value().lower()
    org_name = form['org_name'].value()
    organization = Organization.objects.get(name=org_name)
    user = User.objects.get(email=email)
    
    try:
        Employee.objects.create(
            joined = datetime.now(),
            street_name = form['street_name'].value(),
            street_number = form['street_number'].value(),
            unit_number = form['unit_number'].value(),
            city = form['city'].value(),
            province = form['province'].value(),
            country = form['country'].value(),
            postal = form['postal'].value(),
            email = form['email'].value().lower(),
            phone = form['phone'].value(),
            role = settings.EMPLOYEE_OWNER_ROLE,
            user = user,
            organization = organization,
        )
        return {'status' : 'success', 'message' : 'store registered'}
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering employee.'
    }


def store_registation_successful_page(request):
    return render(request, 'register/store_ok.html',{
        'form': StoreRegistrationForm(),
        'image_form': ImageUploadForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })