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
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
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
        response = client.post('/inventory/webservice/json', {
            'method':'open_cart',
            'id':'1',
            'jsonrpc':'2.0',
            'params': '',
        } ,**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
            
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['result'], 'cart opened')

