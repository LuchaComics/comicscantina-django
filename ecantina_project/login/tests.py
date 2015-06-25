import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from login.views import inventory


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo@gah.com"
TEST_USER_PASSWORD = "ContinentalUnion"


class InventoryLoginTest(TestCase):
    """
        Run in Console:
        python manage.py test login
    """
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()
        Store.objects.all().delete()
        Employee.objects.all().delete()
    
    def setUp(self):
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()
        
        organization = Organization.objects.create(
            name='Galactic Alliance of Humankind',
            description = 'Last humans in all of the galaxy',
            #joined = ''
            street_name='Centre Street',
            street_number='120',
            unit_number='102',
            city='London',
            province='Ontario',
            country='Canada',
            postal='N6J4X4',
            website = 'www.mikasoftware.com',
            email = TEST_USER_EMAIL,
            phone = '519-432-7898',
            fax = '',
            twitter_url = '',
            facebook_url = '',
            instagram_url = '',
            linkedin_url = '',
            github_url = '',
            google_url = '',
            youtube_url = '',
            flickr_url = '',
            administrator = user,
            logo = None,
        )
        
        
        store = Store.objects.create(
            organization=organization,
            store_id=1,
            name='BA Comic\'s',
            description='TEST',
            street_name='Hamilton Rd',
            street_number='426',
            unit_number=None,
            city='London',
            province='Ontario',
            country='Canada',
            postal='N5Z 1R9',
            website='http://www.bacomics.ca',
            email=None,
            phone='519-439-9636',
            fax=None,
        )
        employee = Employee.objects.create(
            organization=organization,
            employee_id=1,
            role=settings.EMPLOYEE_OWNER_ROLE,
            store=store,
            user=user,
        )
    
    def test_root_url_resolves_to_login_page_view(self):
        found = resolve('/inventory/login')
        self.assertEqual(found.func, inventory.login_page)


    def test_login_page_returns_correct_html(self):
        client = Client()
        response = client.post('/inventory/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id_email',response.content)
        self.assertIn(b'id_password',response.content)

    def test_login_authentication_with_succesful_login(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        response = client.post(
            '/inventory/login_authentication',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD},
            **kwargs
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'logged on')


    def test_login_authentication_with_failed_login(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        response = client.post(
            '/inventory/login_authentication',
            {'username': TEST_USER_USERNAME, 'password': 'wrong_password'},
            **kwargs
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'wrong username or password')

    def test_login_authentication_with_suspension(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Suspend User
        user = User.objects.get(username=TEST_USER_USERNAME)
        user.is_active = False
        user.save()
        
        # Test
        client = Client()
        response = client.post(
            '/inventory/login_authentication',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD},
            **kwargs
        )
                               
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'you are suspended')


    def test_logout_authentication_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/logout_authentication', {}, **kwargs )
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'you are logged off')

    def test_login_authentication_with_non_ajax_call(self):
        # Test
        client = Client()
        response = client.post(
            '/inventory/login_authentication',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD}
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'an unknown error occured')

    def test_logout_authentication_with_non_ajax_call(self):
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/logout_authentication')
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'you are logged off')