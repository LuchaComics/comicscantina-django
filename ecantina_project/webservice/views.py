import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User


def ajax_secure_login(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    #    if request.is_ajax():
    #        if request.method == 'POST':
    #            form = ImageUploadForm(request.POST, request.FILES)
    #            if form.is_valid():
    #                form.save()
    #                response_data = {
    #                    'status' : 'success',
    #                    'message' : 'saved',
    #            }
    #            else:
    #                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_add_to_cart(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
#    if request.is_ajax():
#        if request.method == 'POST':
#            form = ImageUploadForm(request.POST, request.FILES)
#            if form.is_valid():
#                form.save()
#                response_data = {
#                    'status' : 'success',
#                    'message' : 'saved',
#            }
#            else:
#                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")