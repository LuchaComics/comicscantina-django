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
from captcha.models import CaptchaStore
from inventory.views import help
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


class HelpTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_help
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)
        now = datetime.now()
    
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    
    def test_url_resolves_to_help_page(self):
        found = resolve('/inventory/1/1/help')
        self.assertEqual(found.func, help.help_page)

    def test_url_resolves_to_ajax_save_image(self):
        found = resolve('/inventory/1/1/help/save_image')
        self.assertEqual(found.func, help.ajax_save_image)

    def test_url_resolves_to_ajax_save_data(self):
        found = resolve('/inventory/1/1/help/save_data')
        self.assertEqual(found.func, help.ajax_save_data)

    def test_help_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b' Contact Us',response.content)
        self.assertIn(b'id_hidden_upload_id',response.content)

    def test_save_image_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/1/1/help/save_image', {
                'upload_id': 1,
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_data_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/help/save_data',{
            'upload_id':'0',
            'subject':'1',
            'subject_url':'http://www.comicascantina.com/help',
            'message':'This is a unit test message.',
        },**KWARGS)
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')