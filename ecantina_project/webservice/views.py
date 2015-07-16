from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import simplejson


@csrf_exempt
def json_rpc_view(request):
    response_data = {'jsonrpc':'2.0', 'id': 666, 'result': 'not post', }
    if request.method == 'POST':
        post = request.body
        post = simplejson.loads(post)
        print(post["jsonrpc"])
        print(post["id"])
        print(post["method"])
        print(post.get("params"))
        response_data = {'id': 6, 'result': 'ok', }
    return JsonResponse(response_data)