import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static, settings
from inventory.views import setting_users
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.section import Section
from inventory.tests.sample import SamplDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class UsersSettingsTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_setting_users
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    def test_url_resolves_to_users_list_settings_page(self):
        found = resolve('/inventory/1/1/settings/users/1')
        self.assertEqual(found.func, setting_users.users_list_settings_page)

    def test_url_resolves_to_edit_user_settings_page(self):
        found = resolve('/inventory/1/1/settings/users/1/1')
        self.assertEqual(found.func, setting_users.edit_user_settings_page)

    def test_url_resolves_to_add_user_settings_page(self):
        found = resolve('/inventory/1/1/settings/users/1/new')
        self.assertEqual(found.func, setting_users.add_user_settings_page)

    def test_url_resolves_to_ajax_save_employee_image(self):
        found = resolve('/inventory/1/1/settings/users/1/1/save_image')
        self.assertEqual(found.func, setting_users.ajax_save_employee_image)

    def test_url_resolves_to_ajax_save_user_data(self):
        found = resolve('/inventory/1/1/settings/users/1/1/save_data')
        self.assertEqual(found.func, setting_users.ajax_save_user_data)

    def test_url_resolves_to_ajax_delete_user(self):
        found = resolve('/inventory/1/1/settings/users/delete/1')
        self.assertEqual(found.func, setting_users.ajax_delete_user)

    def test_url_resolves_to_ajax_assign_employee_to_store(self):
        found = resolve('/inventory/1/1/settings/users/assign_employee')
        self.assertEqual(found.func, setting_users.ajax_assign_employee_to_store)

    def test_users_list_settings_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Users',response.content)
        self.assertIn(b'Add User',response.content)

    def test_ajax_save_employee_image_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/1/1/settings/users/1/1/save_image', {
                'upload_id': 1,
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_ajax_save_user_data_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/1/1/save_data',{
            'email': TEST_USER_EMAIL,
            'role': settings.EMPLOYEE_WORKER_ROLE,
            'name': 'Galactic Alliance of Humankind',
            'upload_id': 1,
            'street_number': 1,
            'street_name': 'Test Street',
            'unit_number': 1,
            'city': 'London',
            'province': 'Ontario',
            'country': 'Canada',
            'postal': 'N6J4X4',
        },**KWARGS)
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_edit_user_settings_page_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Info',response.content)
        self.assertIn(b'Profile Image',response.content)
        

    def test_add_user_settings_page_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/1/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Info',response.content)
        self.assertIn(b'Profile Image',response.content)

    def test_ajax_delete_user_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/delete/1',{},**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

    def test_ajax_assign_employee_to_store_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/users/assign_employee',{
            'this_employee_id': 1,
            'this_store_id': 1,
        },**KWARGS)
                  
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                      
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')
