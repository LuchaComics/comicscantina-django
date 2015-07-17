from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import simplejson


# JSON RPC HANDLER
#-------------------


@csrf_exempt
def json_rpc_view(request):
    response_data = {'jsonrpc':'2.0', 'id': 1, 'result': 'not post', }
    if request.method == 'POST':
        # Attempt to parse the data from a mobile device.
        try:
            #print(repr(request.POST)) # Debugging purposes only
            post = simplejson.loads(request.body)
        except:
            post = None
        
        # If parsing failed, attempt to parse again using a different method.
        if post is None:
            try:
                post = request.POST.dict()
            except:
                # If we still get an exception, then return error.
                return JsonResponse({'id': 1, 'result': 'failed parsing error', })
    
        #print(repr(post)) # Debugging purposes only
        jsonrpc = post.get("jsonrpc")
        id = int(post.get("id"))
        id = id+1
        method = post.get("method")
        params = post.get("params")
        response_data = json_rpc_processor(jsonrpc, id, method, params)
    return JsonResponse(response_data)


def json_rpc_processor(jsonrpc, id, method, params):
    if method == 'hello_world':
        return hello_world(jsonrpc, id, method, params)
    if method == 'add':
        return add(jsonrpc, id, method, params)
    else:
        return {'jsonrpc': '2.0', 'id': 6, 'result': 'method not found', }


# FUNCTIONS
#-------------------


def hello_world(jsonrpc, id, method, params):
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'Hello World!', }


def add(jsonrpc, id, method, params):
    #print(params) # Debugging purposes only
    a = float(params.get("a"))
    b = float(params.get("b"))
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 1, }