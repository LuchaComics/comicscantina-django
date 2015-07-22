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
from inventory.views import print_label
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


class PrintLabelTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_print_label
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
    
    def test_url_resolves_to_print_label_comics_page(self):
        found = resolve('/inventory/1/1/print_label/comics')
        self.assertEqual(found.func, print_label.print_label_comics_page)

    def test_help_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/print_label/comics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics',response.content)