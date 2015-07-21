import simplejson
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from inventory.models.ec.employee import Employee
from inventory.models.ec.store import Store
from inventory.models.ec.cart import Cart
from inventory.models.ec.customer import Customer
from inventory.models.ec.product import Product
from inventory.models.ec.comic import Comic


# JSON RPC VIEW
#-------------------


@csrf_exempt
def json_rpc_view(request):
    response_data = {'jsonrpc':'2.0', 'id': 1, 'result': 'not post', }
    if request.method == 'POST':
        # Parse the request
        post = parse_json(request)
        if post is None:
            return JsonResponse({'id': 1, 'result': 'failed parsing error', })
    
        # Extract the parameters
        jsonrpc = post.get("jsonrpc")
        id = int(post.get("id"))
        id = id+1
        method = post.get("method")
        params = post.get("params")

        # Process the request
        if method == 'hello_world':
            return JsonResponse(hello_world(jsonrpc, id, method, params))
        elif method == 'add':
            return JsonResponse(add(jsonrpc, id, method, params))
        elif method == 'login':
            return JsonResponse(employee_login(request, jsonrpc, id, method, params))
        elif method == 'logout':
            return JsonResponse(employee_logout(request, jsonrpc, id, method, params))
        else:
            return JsonResponse({'jsonrpc': '2.0', 'id': 6, 'result': 'method not found', })


@login_required()
@csrf_exempt
def json_rpc_secure_view(request):
    response_data = {'jsonrpc':'2.0', 'id': 1, 'result': 'not post', }
    if request.method == 'POST':
        # Parse the request
        post = parse_json(request)
        if post is None:
            return JsonResponse({'id': 1, 'result': 'failed parsing error', })
        
        # Extract the parameters
        jsonrpc = post.get("jsonrpc")
        id = int(post.get("id"))
        id = id+1
        method = post.get("method")
        params = post.get("params")
        
        # Process the request
        if method == 'cashier_logout':
            return JsonResponse(cashier_logout(request, jsonrpc, id, method, params))
        elif method == 'open_cart':
            return JsonResponse(open_cart(request, jsonrpc, id, method, params))
        elif method == 'assign_cart':
            return JsonResponse(assign_cart(request, jsonrpc, id, method, params))
        elif method == 'add_product_to_cart':
            return JsonResponse(add_product_to_cart(request, jsonrpc, id, method, params))
        elif method == 'remove_product_from_cart':
            return JsonResponse(remove_product_from_cart(request, jsonrpc, id, method, params))
        elif method == 'checkout_cart':
            return JsonResponse(checkout_cart(request, jsonrpc, id, method, params))
        elif method == 'add_to_checkedout_cart':
            return JsonResponse(add_to_checkedout_cart(request, jsonrpc, id, method, params))
        else:
            return JsonResponse({'jsonrpc': '2.0', 'id': 6, 'result': 'method not found', })
    return JsonResponse(response_data)


# JSON RPC HANDLER
#-------------------


def parse_json(request):
    """
        Function process the JSON request data from either a mobile
        device or django and returns a python dictionary. Returns None
        if the parsing failed.
    """
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
            return None
    return post


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


def employee_login(request, jsonrpc, id, method, params):
    """
        Authenticate the user and log them into the system and start a 
        session for the use.
    """
    try:
        username = params.get("username")
        password = params.get("password")
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed logging in b/c params', }
    user = authenticate(
        username=username.lower(),
        password=password
    )
    # Perform a battery of tests on the user account to ensure
    # it meets the requirements for logging into our system.
    response_data = validate_user(user)
        
    # If user meets requirements then offically login the user.
    if response_data['status'] == 'success':
        login(request, user)
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'success', }
    else:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed logging in', }


def validate_user(user):
    if user is not None:
        if user.is_active:
            try:
                # Get the employee and return the first store in the organization.
                employee = Employee.objects.get(user=user)
                store = Store.objects.filter(organization=employee.organization)[0]
                return {
                    'status': 'success',
                    'message': 'logged on',
                    'org_id': employee.organization.org_id,
                    'store_id': store.store_id,
                }
            except Employee.DoesNotExist:
                return {'status' : 'failure', 'message' : 'you are not an employee'}
        else:
            return {'status' : 'failure', 'message' : 'you are suspended'}
    else:
        return {'status' : 'failure', 'message' : 'wrong username or password'}


def employee_logout(request, jsonrpc, id, method, params):
    """
        Close the session for the user.
    """
    try:
        logout(request)
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'success', }
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed logging out', }


def open_cart(request, jsonrpc, id, method, params):
    """
        Opens a new cart to be loaded in by the store employee. If a previous
        cart existed it will be deleted.
    """
    # Close the previous cart if it exist for the current customer / employee
    employee = Employee.objects.get(user=request.user)
    q = Cart.objects.filter(employee=employee)
    q = q.filter(is_closed=False)
    for cart in q:
        cart.is_closed = True
        cart.save()
    
    # Open a new cart.
    try:
        cart = Cart.objects.create(
            employee = employee,
            created = datetime.now(),
        )
        return {'jsonrpc': jsonrpc, 'id': id, 'result': cart.cart_id }
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': -1, }


def assign_cart(request, jsonrpc, id, method, params):
    """
        Assign a customer to the current cart.
    """
    try:
        customer_id = int(params.get("customer_id"))
        customer = Customer.objects.get(customer_id=customer_id)
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: customer not found', }

    try:
        cart_id = int(params.get("cart_id"))
        cart = Cart.objects.get(cart_id=cart_id)
        cart.customer = customer
        cart.save()
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'success', }
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot find cart', }


def add_product_to_cart(request, jsonrpc, id, method, params):
    """
        Assign a product to the current cart.
    """
    # Attempt to load the parameters
    try:
        product_id = int(params.get("product_id"))
        cart_id = int(params.get("cart_id"))
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: customer not found', }
    
    # Attempt to find the product.
    try:
        product = Product.objects.get(product_id=product_id)
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot find product', }

    # Attempt to find the cart.
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot find cart', }

    # Create the cart item.
    try:
        cart.products.add(product)
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'success', }
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot add product to cart', }


def remove_product_from_cart(request, jsonrpc, id, method, params):
    """
        Removes a product from the current cart.
    """
    # Attempt to load the parameters
    try:
        product_id = int(params.get("product_id"))
        cart_id = int(params.get("cart_id"))
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: customer not found', }
    
    # Attempt to find the product.
    try:
        product = Product.objects.get(product_id=product_id)
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot find product', }
    
    # Attempt to find the cart.
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot find cart', }
    
    # Remove the cart item.
    try:
        cart.products.remove(product)
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'success', }
    except:
        return {'jsonrpc': jsonrpc, 'id': id, 'result': 'failed: cannot add product to cart', }


def checkout_cart(request, jsonrpc, id, method, params):
    """
        Close the cart and tell the system to handle dealing with a
        finished purchasing session.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }


def add_to_checkedout_cart(request, jsonrpc, id, method, params):
    """
        Assign a product to the cart which was previously checked out.
    """
    return {'jsonrpc': jsonrpc, 'id': id, 'result': 'todo', }