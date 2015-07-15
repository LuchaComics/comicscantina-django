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


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo@gah.com"
TEST_USER_PASSWORD = "ContinentalUnion"
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
    
    def test_url_resolves_to_ajax_add_to_cart_view(self):
        found = resolve('/inventory/webservice/add_to_cart')
        self.assertEqual(found.func, views.ajax_add_to_cart)

##Todo!
#    def test_login_authentication_with_succesful_login(self):
#        # Extra parameters to make this a Ajax style request.
#        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
#        
#        # Test
#        client = Client()
#        response = client.post(
#            '/inventory/login_authentication',
#            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD},
#                            **kwargs
#        )
#                               
#        # Verify: Check that the response is 200 OK.
#        self.assertEqual(response.status_code, 200)
#                               
#        # Verify: Successful response.
#        json_string = response.content.decode(encoding='UTF-8')
#        array = json.loads(json_string)
#        self.assertEqual(array['status'], 'success')
#        self.assertEqual(array['message'], 'logged on')

    def test_save_org_data_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/webservice/add_to_cart',{
                               
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'added to cart')
        self.assertEqual(array['status'], 'success')
