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
from captcha.models import CaptchaStore
from . import views
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class RegistrationTestCase(TestCase):
    """
        Run in Console:
        python manage.py test register
    """
    def tearDown(self):
        User.objects.all().delete()
        for image in ImageUpload.objects.all():
            image.delete()
        for org in Organization.objects.all():
            org.delete()
        for store in Store.objects.all():
            store.delete()
        for employee in Employee.objects.all():
            employee.delete()
    
    def setUp(self):
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)
    
    def test_url_resolves_to_store_registration_page(self):
        found = resolve('/inventory/register')
        self.assertEqual(found.func, views.store_registration_page)

    def test_url_resolves_to_ajax_store_save_image(self):
        found = resolve('/inventory/save_image')
        self.assertEqual(found.func, views.ajax_store_save_image)

    def test_url_resolves_to_ajax_create_account(self):
        found = resolve('/inventory/create_account')
        self.assertEqual(found.func, views.ajax_create_account)
    
    def test_url_resolves_to_store_registation_successful_page(self):
        found = resolve('/inventory/registered_successful')
        self.assertEqual(found.func, views.store_registation_successful_page)

    def test_store_registration_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/register', { })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id_org_name',response.content)
        self.assertIn(b'id_password',response.content)


    def test_save_image_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/save_image', {
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')


    def test_register_with_succesful_login(self):
        image = ImageUpload.objects.create(
            upload_id = 1,
            image = None,
            user =None,
        )
        
        # Developer Notes:
        # To get unit tests working with the django-simple-captcha then follow:
        # http://stackoverflow.com/questions/3159284/how-to-unit-test-a-form-with-a-captcha-field-in-django
        
        # Test
        client = Client()
        response = client.post('/inventory/create_account',{
            'hidden_upload_id': image.upload_id,
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
            'repeat_password': TEST_USER_PASSWORD,
            'first_name': 'Ledo',
            'last_name': 'Dunno',
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
        self.assertEqual(array['message'], 'successfully registered')
        self.assertEqual(array['status'], 'success')
                               
        # Verify: Database updated
        try:
            user = User.objects.get(email=TEST_USER_EMAIL)
        except User.DoesNotExist:
            user = None
        self.assertEqual(user.username, TEST_USER_EMAIL)

    def test_store_registation_successful_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/registered_successful', { })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login',response.content)
        self.assertIn(b'inventory',response.content)