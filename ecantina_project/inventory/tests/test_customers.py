import json
from datetime import datetime
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static, settings
from django.db import IntegrityError, transaction
from inventory.views import customers
from api.models.ec.imageupload import ImageUpload
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from inventory.tests.sample import SamplDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class CustomersTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_customers
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
        for customer in Customer.objects.all():
            customer.delete()
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    def test_url_resolves_to_help_page(self):
        found = resolve('/inventory/1/1/customers')
        self.assertEqual(found.func, customers.customers_page)

    def test_url_resolves_to_ajax_refresh_table(self):
        found = resolve('/inventory/1/1/customers/refresh_table')
        self.assertEqual(found.func, customers.ajax_refresh_table)

    def test_url_resolves_to_ajax_delete_customer(self):
        found = resolve('/inventory/1/1/customers/delete')
        self.assertEqual(found.func, customers.ajax_delete_customer)

    def test_url_resolves_to_add_customer_page(self):
        found = resolve('/inventory/1/1/add_customer')
        self.assertEqual(found.func, customers.add_customer_page)

    def test_url_resolves_to_ajax_add_customer(self):
        found = resolve('/inventory/1/1/add_customer/submit')
        self.assertEqual(found.func, customers.ajax_add_customer)

    def test_customers_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer List',response.content)
        self.assertIn(b'ajax_placeholder',response.content)

    def test_add_customer_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add_customer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Customer',response.content)
        self.assertIn(b'ajax_submit();',response.content)

    def test_ajax_refresh_table_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customers/refresh_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Privacy Consent',response.content)
        self.assertIn(b'Email',response.content)

    def test_ajax_delete_customer_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Create test data.
        response = client.post('/inventory/1/1/add_customer/submit',{
            'first_name':'Main Store12',
            'last_name':'Tes12t',
            'joined':'2015-01-01',
            'street_name':'Hamilton Rd',
            'street_number':'426',
            'unit_number':'1',
            'city':'London',
            'province':'Ontario',
            'country':'Canada',
            'postal':'N5Z 1R9',
            'email':'123test123@testing.com',
            'phone':'519-439-9636',
        },**KWARGS)
        
        # Test
        response = client.post('/inventory/1/1/customers/delete',{
            'customer_id':'2',
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_ajax_add_customer_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                response = client.post('/inventory/1/1/add_customer/submit',{
                    'first_name':'Main Store123',
                    'last_name':'Tes12t4',
                    'joined':'2015-01-02',
                    'street_name':'Hamilton Rd',
                    'street_number':'427',
                    'unit_number':'2',
                    'city':'London',
                    'province':'Ontario',
                    'country':'Canada',
                    'postal':'N5Z 1R9',
                    'email':'123test1231@testing.com',
                    'phone':'519-439-9636',
                },**KWARGS)
    
                # Verify: Check that the response is 200 OK.
                self.assertEqual(response.status_code, 200)
        
                # Verify: Successful response.
                json_string = response.content.decode(encoding='UTF-8')
                array = json.loads(json_string)
                self.assertEqual(array['message'], 'saved')
                self.assertEqual(array['status'], 'success')
        except IntegrityError:
            self.assertEqual(True,False)
