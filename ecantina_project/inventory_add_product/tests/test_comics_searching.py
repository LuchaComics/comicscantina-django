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
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue
from api.models.gcd.story import GCDStory
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from inventory.tests.sample import SamplDataPopulator
from inventory_add_product.views import search_comic

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class ComicsSearchTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_add_product.tests.test_comics_searching
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)
    
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    
    def test_url_resolves_to_search_comics_page(self):
        found = resolve('/inventory/1/1/add/comic')
        self.assertEqual(found.func, search_comic.search_comics_page)

    def test_url_resolves_to_ajax_search_comics(self):
        found = resolve('/inventory/1/1/add/search_comics')
        self.assertEqual(found.func, search_comic.ajax_search_comics)

    def test_search_comics_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_search_results_placeholder',response.content)
        self.assertIn(b'id_issue',response.content)
        self.assertIn(b'id_series',response.content)


    def test_ajax_search_comics_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/search_comics',{
            'series': 'Winter World',
            'issue_num': '',
            'publisher': '',
            'genre': '',
            'from': '',
            'to': '',
        },**KWARGS)
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify Results.
        self.assertIn(b'1 Results Listed',response.content)
