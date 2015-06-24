import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from register.forms import StoreRegistrationForm
from inventory.forms.imageuploadform import ImageUploadForm
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization


def store_registration_page(request):
    return render(request, 'register/store.html',{
        'form': StoreRegistrationForm(),
        'image_form': ImageUploadForm(),
        'local_css_library' : settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header' : settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body' : settings.INVENTORY_JS_LIBRARY_BODY,
    })


def store_save_image(request):
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


def create_account(request):
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

    # Return successful status
    response_data = {
        'status' : 'success',
        'message' : 'successfully registered'
    }
    return response_data


def create_user(form):
    email = form['email'].value().lower()
    first_name = form['first_name'].value()
    last_name = form['last_name'].value()
    password = form['password'].value()
    repeat_password = form['repeat_password'].value()
        
    # Create the user in our database
    try:
        user = User.objects.create_user(
            email,  # Username
            email,  # Email
            password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering user.'
        }
    response_data = {'status' : 'success', 'message' : 'user registered'}
    return response_data


def create_organization(form):
    # Get administrator
    email = form['email'].value().lower()
    administrator = User.objects.get(email=email)
    
    # Get contact & basic
    store_name = form['store_name'].value()
    phone = form['phone'].value()
    fax = form['fax'].value()
    website = form['website'].value()
    twitter = form['twitter'].value()
    facebook = form['facebook'].value()
    upload_id = int(form['hidden_upload_id'].value())
    image_upload = ImageUpload.objects.get(upload_id=upload_id)

    # Get location
    street_number = form['street_number'].value()
    street_name = form['street_name'].value()
    unit_number = form['unit_number'].value()
    city = form['city'].value()
    province = form['province'].value()
    country = form['country'].value()
    postal = form['postal'].value()

    # Create organization
    try:
        Organization.objects.create(
            logo=image_upload,
            administrator=administrator,
            name=store_name,
            street_number=street_number,
            street_name=street_name,
            unit_number=unit_number,
            city=city,
            province=province,
            country=country,
            postal=postal,
            phone=phone,
            fax=fax,
            website=website,
            twitter_url=twitter,
            facebook_url=facebook,
        )
        return {'status' : 'success', 'message' : 'user registered'}
    except:
        return {
            'status' : 'failure',
            'message' : 'an unknown error occured when creating organization'
        }
    return response_data
