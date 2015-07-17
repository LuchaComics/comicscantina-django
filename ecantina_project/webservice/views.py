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
            #print('Raw Data: %s' % request.body )# Debugging Purposes Only.
            post = simplejson.loads(request.body)
        except:
            post = None
        
        # If parsing failed, attempt to parse again using a different method.
        if post is None:
            try:
                post = request.POST.dict()
                
                # Attempt to convert the parameters into a python dictionary
                # if it fails that's ok, just skip this step.
                try:
                    post['params'] = simplejson.loads(post.get("params"))
                    #print(post) # Debugging purposes only
                except:
                    pass
            except:
                return JsonResponse({'id': 1, 'result': 'failed parsing error', })
    
        # Extract the parameters
        jsonrpc = post.get("jsonrpc")
        id = int(post.get("id"))
        id = id+1
        method = post.get("method")
        params = post.get("params")
        
        # Process the request.
        response_data = process_request(jsonrpc, id, method, params)
    return JsonResponse(response_data)


def process_request(jsonrpc, id, method, params):
    if method == 'hello_world':
        return hello_world(jsonrpc, id, method, params)
    if method == 'add':
        return add(jsonrpc, id, method, params)
    else:
        return {'jsonrpc': '2.0', 'id': 6, 'result': 'method not found', }


# FUNCTIONS
#-------------------


def hello_world(jsonrpc, id, method, params):
    """
        Test function used by developers to test out making JSON-RPC calls
        for learning and testing purposes which won't break anything.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'Hello World!', }


def add(jsonrpc, id, method, params):
    """
        Test function used by developers to test out making JSON-RPC calls
        involving parameters.
    """
    try:
        a = float(params.get("a"))
    except:
        a = 0
    try:
        b = float(params.get("b"))
    except:
        b = 0
    return {'jsonrpc': jsonrpc, 'id': id, 'result': a+b, }


def open_cart(jsonrpc, id, method, params):
    """
        Opens a new cart to be loaded in by the store employee. If a previous
        cart existed it will be deleted.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }


def assign_cart(jsonrpc, id, method, params):
    """
        Assign a customer to the current cart.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }


def add_to_cart(jsonrpc, id, method, params):
    """
        Assign a product to the current cart.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }


def checkout_cart(jsonrpc, id, method, params):
    """
        Close the cart and tell the system to handle dealing with a
        finished purchasing session.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }


def add_to_checkedout_cart(jsonrpc, id, method, params):
    """
        Assign a product to the cart which was previously checked out.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }