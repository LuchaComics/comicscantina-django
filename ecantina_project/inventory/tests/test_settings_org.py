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
from inventory.views import setting
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.location import Location
from inventory.models.ec.section import Section


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class OrganizationSettingsTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_settings_org
    """
    def tearDown(self):
        for image in ImageUpload.objects.all():
            image.delete()
        for org in Organization.objects.all():
            org.delete()
        for store in Store.objects.all():
            store.delete()
        for employee in Employee.objects.all():
            employee.delete()
        User.objects.all().delete()
    
    def setUp(self):
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)
        now = datetime.now()
        
        #----------------
        # Administrator
        #----------------
        try:
            user = User.objects.create_user(
                TEST_USER_EMAIL,  # Username
                TEST_USER_EMAIL,  # Email
                TEST_USER_PASSWORD,
            )
            user.is_active = True
            user.save()
        except Exception as e:
            user = User.objects.get(email=TEST_USER_EMAIL)
    
        #----------------
        # Image Uploads
        #----------------
        logo = None
        profile = None
            
        #-----------------
        # Organization
        #-----------------
        try:
            organization = Organization.objects.create(
                org_id=1,
                name='B.A.\'s Comics',
                description = 'Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
                joined = now,
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
                twitter_url='https://twitter.com/bascomics',
                facebook_url=None,
                instagram_url=None,
                linkedin_url=None,
                github_url=None,
                google_url='https://plus.google.com/105760942218297346537/about',
                youtube_url=None,
                flickr_url=None,
                administrator = user,
                logo = logo,
            )
        except Exception as e:
            organization = Organization.objects.get(org_id=1)
                                                                          
        #-----------------
        # Store
        #-----------------
        try:
            store = Store.objects.create(
            store_id=1,
            name='Main Store',
            description='Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
            joined=now,
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
            organization=organization,
            )
        except Exception as e:
            store = Store.objects.get(store_id=1)

        #-----------------
        # Employees
        #-----------------
        try:
            Employee.objects.create(
                employee_id=1,
                role = settings.EMPLOYEE_OWNER_ROLE,
                store = store,
                user = user,
                organization = organization,
                profile=profile,
            )
        except Exception as e:
            pass
    
    def test_url_resolves_to_org_settings_page(self):
        found = resolve('/inventory/1/1/settings/organization')
        self.assertEqual(found.func, setting.org_settings_page)

    def test_url_resolves_to_ajax_store_save_image(self):
        found = resolve('/inventory/1/1/settings/save_org_logo')
        self.assertEqual(found.func, setting.ajax_org_save_logo)

    def test_url_resolves_to_ajax_save_org_data(self):
        found = resolve('/inventory/1/1/settings/save_org_data')
        self.assertEqual(found.func, setting.ajax_save_org_data)

    def test_org_settings_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/organization')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Organization Settings',response.content)
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
        # Developer Notes:
        # To get unit tests working with the django-simple-captcha then follow:
        # http://stackoverflow.com/questions/3159284/how-to-unit-test-a-form-with-a-captcha-field-in-django
        
        # Test
        client = Client()
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