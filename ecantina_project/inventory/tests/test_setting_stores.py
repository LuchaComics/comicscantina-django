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
from inventory.views import setting_stores
from api.models.ec.imageupload import ImageUpload
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


class StoresSettingsTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_setting_stores
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    def test_url_resolves_to_store_settings_page(self):
        found = resolve('/inventory/1/1/settings/store/1')
        self.assertEqual(found.func, setting_stores.edit_store_settings_page)

    def test_url_resolves_to_ajax_save_store_logo(self):
        found = resolve('/inventory/1/1/settings/store/1/save_logo')
        self.assertEqual(found.func, setting_stores.ajax_save_store_logo)

    def test_url_resolves_to_ajax_save_store_data(self):
        found = resolve('/inventory/1/1/settings/store/1/save_data')
        self.assertEqual(found.func, setting_stores.ajax_save_store_data)

    def test_url_resolves_to_ajax_section(self):
        found = resolve('/inventory/1/1/settings/store/1/section')
        self.assertEqual(found.func, setting_stores.ajax_section)

    def test_url_resolves_to_ajax_delete_section(self):
        found = resolve('/inventory/1/1/settings/store/1/delete_section')
        self.assertEqual(found.func, setting_stores.ajax_delete_section)

    def test_url_resolves_to_ajax_refresh_sections(self):
        found = resolve('/inventory/1/1/settings/store/1/refresh_sections')
        self.assertEqual(found.func, setting_stores.ajax_refresh_sections)

    def test_url_resolves_to_store_settings_page(self):
        found = resolve('/inventory/1/1/settings/store/new')
        self.assertEqual(found.func, setting_stores.store_settings_page)

    def test_edit_store_settings_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Store',response.content)
        self.assertIn(b'id_name',response.content)

    def test_ajax_save_store_logo_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/1/1/settings/store/1/save_logo', {
                'upload_id': 1,
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_store_data_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/1/save_data',{
            'email': TEST_USER_EMAIL,
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

    def test_ajax_section_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/1/section',{
            'section_id': 1,
            'name': 'Galactic Alliance of Humankind',
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_ajax_delete_section_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/1/delete_section',{
            'section_id': 1,
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')
    
    def test_ajax_refresh_sections_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/1/refresh_sections',{},**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        self.assertIn(b'id_section_id_1',response.content)
        self.assertIn(b'id_section_id_2',response.content)

    def test_store_settings_page_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/store/new',{},**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        self.assertIn(b'Store',response.content)
        self.assertIn(b'id_name',response.content)