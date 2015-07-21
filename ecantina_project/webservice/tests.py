import json
from datetime import datetime
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from inventory.models.gcd.series import Series
from inventory.models.gcd.issue import Issue
from inventory.models.gcd.story import Story
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.section import Section
from inventory.models.ec.comic import Comic
from inventory.models.ec.customer import Customer
from inventory.models.ec.cart import Cart
from inventory.models.ec.product import Product
from . import views
from inventory.tests.sample import SamplDataPopulator
import urllib3

TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo@gah.com"
TEST_USER_PASSWORD = "password"
# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class WebServiceTest(TestCase):
    """
        Run in Console:
        python manage.py test webservice
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
        for cart in Cart.objects.all():
            cart.delete()
                
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
        # Create comic & product
        Comic.objects.create(
            comic_id = 1,
            created = '2015-01-01',
            is_cgc_rated = True,
            age = 1,
            cgc_rating = 1,
            label_colour = '',
            condition_rating = 1,
            is_canadian_priced_variant = True,
            is_variant_cover = False,
            is_retail_incentive_variant = False,
            is_newsstand_edition = False,
            price = 1,
            cost = 1,
            issue = Issue.objects.get(issue_id=1),
            organization = Organization.objects.get(org_id=1),
            store = Store.objects.get(store_id=1),
            section = Section.objects.get(section_id=1),
        )
        Product.objects.create(
            product_id = 1,
            type =1,
            comic = Comic.objects.get(comic_id=1),
        )
    
    def test_url_resolves_to_json_secure_webservice_view(self):
        found = resolve('/inventory/webservice/json')
        self.assertEqual(found.func, views.json_rpc_secure_view)
    
    def test_url_resolves_to_json_webservice_view(self):
        found = resolve('/inventory/webservice/auth/json')
        self.assertEqual(found.func, views.json_rpc_view)

    def test_hello_world_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/webservice/auth/json',{
            'jsonrpc':'2.0',
            'id':'1',
            'method':'hello_world',
            'params':'',
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'Hello World!')

    def test_add_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/webservice/auth/json', {
            'method':'add',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({'a': 1, 'b': 2}),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 3)

    def test_logout_without_login_with_authorization_required(self):
        client = Client()
        response = client.post('/inventory/webservice/auth/json', {
            'method':'logout',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    def test_login_with_success(self):
        client = Client()
        response = client.post('/inventory/webservice/auth/json', {
            'method':'login',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'username': TEST_USER_USERNAME,
                'password': TEST_USER_PASSWORD
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                               
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'success')

    def test_logout_with_login_with_success(self):
        client = Client()
        response = client.post('/inventory/webservice/auth/json', {
            'method':'login',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                    'username': TEST_USER_USERNAME,
                    'password': TEST_USER_PASSWORD
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                               
        # Verify: Check that the response is 200 Success.
        self.assertEqual(response.status_code, 200)
                               
        response = client.post('/inventory/webservice/auth/json', {
            'method':'logout',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                               
        # Verify: Check that the response is 200 Success.
        self.assertEqual(response.status_code, 200)
    
    def test_open_cart_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        self.assertEqual(Cart.objects.all().count(), 0)
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
            
        # Verify: Database.
        self.assertEqual(Cart.objects.all().count(), 1)

    def test_assign_cart_with_success(self):
        # Setup
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        self.assertEqual(Cart.objects.all().count(), 0)
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(Cart.objects.all().count(), 1)
        
        # Test
        response = client.post('/inventory/webservice/json', {
            'method':'assign_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({'customer_id': 1,'cart_id':array['result']}),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'success')

    def test_add_product_to_cart_with_success(self):
        # Setup
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        # Create Cart
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content.decode(encoding='UTF-8'))
                     
        # Test
        response = client.post('/inventory/webservice/json', {
            'method':'add_product_to_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'success')

    def test_remove_product_from_cart_with_success(self):
        # Setup
        client = Client()
        client.login(
                     username=TEST_USER_USERNAME,
                     password=TEST_USER_PASSWORD
        )
        # Create Cart
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content.decode(encoding='UTF-8'))
                     
        # Add Product to Cart.
        response = client.post('/inventory/webservice/json', {
            'method':'add_product_to_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)

        # Test
        response = client.post('/inventory/webservice/json', {
                'method':'remove_product_from_cart',
                'id':'1',
                'jsonrpc':'2.0',
                'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'success')

    def test_close_cart_with_success(self):
        # Setup
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        # Create Cart
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content.decode(encoding='UTF-8'))
                     
        # Add Product to Cart.
        response = client.post('/inventory/webservice/json', {
            'method':'add_product_to_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
                     
        # Test
        response = client.post('/inventory/webservice/json', {
            'method':'close_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'success')

    def test_is_cart_closed_with_success(self):
        # Setup
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Create Cart
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content.decode(encoding='UTF-8'))
                     
        # Add Product to Cart.
        response = client.post('/inventory/webservice/json', {
            'method':'add_product_to_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
                'product_id': '1',
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
                     
        # Close Cart
        response = client.post('/inventory/webservice/json', {
            'method':'close_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)

        # Test
        response = client.post('/inventory/webservice/json', {
            'method':'is_cart_closed',
            'id':'1',
            'jsonrpc':'2.0',
            'params': json.dumps({
                'cart_id': 1,'cart_id':array['result'],
            }),
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], True)

