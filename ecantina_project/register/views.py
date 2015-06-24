import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from register.forms import StoreRegistrationForm
from inventory.forms.imageuploadform import ImageUploadForm


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