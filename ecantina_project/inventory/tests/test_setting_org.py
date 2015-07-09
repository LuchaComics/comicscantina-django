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
from inventory.views import setting_org
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


class OrganizationSettingsTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_setting_org
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        now = datetime.now()
    
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    
    def test_url_resolves_to_org_settings_page(self):
        found = resolve('/inventory/1/1/settings/organization')
        self.assertEqual(found.func, setting_org.org_settings_page)

    def test_url_resolves_to_ajax_store_save_image(self):
        found = resolve('/inventory/1/1/settings/save_org_logo')
        self.assertEqual(found.func, setting_org.ajax_org_save_logo)

    def test_url_resolves_to_ajax_save_org_data(self):
        found = resolve('/inventory/1/1/settings/save_org_data')
        self.assertEqual(found.func, setting_org.ajax_save_org_data)

    def test_org_settings_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/organization')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Organization',response.content)
        self.assertIn(b'id_name',response.content)

    def test_save_org_logo_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/1/1/settings/save_org_logo', {
                'upload_id': 1,
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_org_data_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/save_org_data',{
            'email': TEST_USER_EMAIL,
            'name': TEST_USER_USERNAME,
            'upload_id': 1,
            'street_number': 1,
            'street_name': 'Test Street',
            'unit_number': 1,
            'city': 'London',
            'province': 'Ontario',
            'country': 'Canada',
            'postal': 'N6J4X4',
            'org_name': 'Galactic Alliance of Humankind',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        },**KWARGS)
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')
                               
        # Verify: Database updated
        try:
            user = User.objects.get(email=TEST_USER_EMAIL)
        except User.DoesNotExist:
            user = None
        self.assertEqual(user.username, TEST_USER_EMAIL)