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
            post = simplejson.loads(request.body)
        except:
            #print(repr(request.POST))
            post = None
        
        # If parsing failed, attempt to parse again using a different method.
        if post is None:
            try:
                post = request.POST.dict()
            except:
                # If we still get an exception, then return error.
                return JsonResponse({'id': 1, 'result': 'failed parsing error', })
                    
        jsonrpc = post.get("jsonrpc")
        id = post.get("id")
        method = post.get("method")
        params = post.get("params")
        response_data = json_rpc_processor(jsonrpc, id, method, params)
    return JsonResponse(response_data)


def json_rpc_processor(jsonrpc, id, method, params):
    return {'jsonrpc': '2.0', 'id': 6, 'result': 'ok', }


# FUNCTIONS
#-------------------