import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.helprequest import HelpRequest
from inventory.forms.imageuploadform import ImageUploadForm
from inventory.forms.helprequestform import HelpRequestForm


@login_required(login_url='/inventory/login')
def help_page(request, org_id, store_id):
    return render(request, 'inventory_help/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': HelpRequestForm(),
        'tab':'help',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def ajax_save_image(request, org_id, store_id):
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
                
                response_data = {  # Return status.
                    'status' : 'success',
                    'message' : 'saved',
                    'src': form.instance.image.url,
                    'id': form.instance.upload_id,
            }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_save_data(request, org_id, store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            form = HelpRequestForm(request.POST)
            form.instance.organization = Organization.objects.get(org_id=org_id)
            form.instance.store = Store.objects.get(store_id=store_id)
            form.instance.employee = Employee.objects.get(user=request.user)
            if form.is_valid() is False:
                response_data = {
                    'status': 'failed',
                    'message': json.dumps(form.errors),
                }
            else:
                try:
                    upload_id = request.POST['upload_id']
                    upload = None
                    if upload_id is not '':
                        upload = ImageUpload.objects.get(upload_id=int(upload_id))
                        form.instance.screenshot = upload
                except ImageUpload.DoesNotExist:
                    pass
                form.save()
                response_data = {
                    'status': 'success',
                    'message': 'saved',
                    'id': form.instance.help_id,
                }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

