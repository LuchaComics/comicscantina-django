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
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue
from api.models.gcd.story import Story
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from inventory.tests.sample import SamplDataPopulator
from inventory_add_product.views import add_comic
from inventory_add_product.forms import ProductForm


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class ComicsAddTest(TestCase):
    """
        Run in Console:
        python manage.py test inventory_add_product.tests.test_comics_add
    """
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    def test_url_resolves_to_add_product_page(self):
        found = resolve('/inventory/1/1/add/comic/1/product/0')
        self.assertEqual(found.func, add_comic.comic_page)

    def test_url_resolves_to_list_products(self):
        found = resolve('/inventory/1/1/add/comic/1/list_products')
        self.assertEqual(found.func, add_comic.list_products)

    def test_url_resolves_to_ajax_save_uploaded_cover(self):
        found = resolve('/inventory/1/1/add/comic/1/upload_cover')
        self.assertEqual(found.func, add_comic.ajax_save_uploaded_cover)

    def test_url_resolves_to_ajax_add_product(self):
        found = resolve('/inventory/1/1/add/comic/1/add_product')
        self.assertEqual(found.func, add_comic.ajax_add_product)

    def test_url_resolves_to_ajax_sections_per_store(self):
        found = resolve('/inventory/1/1/add/comic/1/section_dropbox/1')
        self.assertEqual(found.func, add_comic.ajax_sections_per_store)

    def test_url_resolves_to_ajax_delete_comic(self):
        found = resolve('/inventory/1/1/add/comic/1/delete/1')
        self.assertEqual(found.func, add_comic.ajax_delete_comic)

    def test_add_product_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/product/0')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Winter World (2015 series)',response.content)
        self.assertIn(b'id_table_placeholder',response.content)
        self.assertIn(b'id_hidden_upload_id',response.content)

    def test_list_products_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/list_products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory Items',response.content)
        self.assertIn(b'<table',response.content)

    def test_ajax_save_employee_image_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/1/1/add/comic/1/upload_cover', {
                'upload_id': 1,
                'image': fp,
            }, **KWARGS)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_ajax_add_product_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/add_product',{
            'comic_id': '0',
                               'type': 1,
            'upload_id': '1',
            'age':'1',
            'is_cgc_rated':'',
            'cgc_rating':'',
            'label_colour':'',
            'condition_rating':'1',
            'is_canadian_priced_variant':'true',
            'is_variant_cover':'true',
            'is_retail_incentive_variant':'true',
            'is_newsstand_edition':'true',
            'price':'',
            'price':'',
            'cost':'',
            'section':'1',
            'store':'1',
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify Results.
        self.assertIn(b'saved',response.content)
    
        # Verify database.
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(Comic.objects.all().count(), 1)


    def test_ajax_sections_per_store_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/section_dropbox/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id_section',response.content)
        self.assertIn(b'<select',response.content)

    def test_ajax_delete_comic_with_success(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Create product for testing.
        response = client.post('/inventory/1/1/add/comic/1/add_product',{
            'comic_id': '0',
            'type': 1,
            'upload_id': '1',
            'age':'1',
            'is_cgc_rated':'',
            'cgc_rating':'',
            'label_colour':'',
            'condition_rating':'1',
            'is_canadian_priced_variant':'true',
            'is_variant_cover':'true',
            'is_retail_incentive_variant':'true',
            'is_newsstand_edition':'true',
            'price':'',
            'price':'',
            'cost':'',
            'section':'1',
            'store':'1',
        },**KWARGS)
                               
        # Verify test data was loaded.
        self.assertEqual(response.status_code, 200)
        
        # Test & Verify.
        comic = Comic.objects.all()[0]
        response = client.post('/inventory/1/1/add/comic/1/delete/'+str(comic.comic_id),{
        },**KWARGS)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify Results.
        self.assertIn(b'deleted',response.content)
    
        # Verify database.
        self.assertEqual(Product.objects.all().count(), 0)
        self.assertEqual(Comic.objects.all().count(), 0)

    def test_edit_product_with_success(self):
        # Setup.
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/add_product',{
            'comic_id': '0',
            'type': 1,
            'upload_id': '1',
            'age':'1',
            'is_cgc_rated':'',
            'cgc_rating':'',
            'label_colour':'',
            'condition_rating':'1',
            'is_canadian_priced_variant':'true',
            'is_variant_cover':'true',
            'is_retail_incentive_variant':'true',
            'is_newsstand_edition':'true',
            'price':'45',
            'cost':'666',
            'section':'1',
            'store':'1',
        },**KWARGS)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'saved',response.content)

        # Test & Verify.
        comic = Comic.objects.all()[0]
        response = client.post('/inventory/1/1/add/comic/1/product/'+str(comic.comic_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Winter World (2015 series)',response.content)
        self.assertIn(b'45',response.content)
        self.assertIn(b'666',response.content)

    def test_edit_and_edit_product_with_success(self):
        # Setup.
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add/comic/1/add_product',{
            'comic_id': '0',
            'type': 1,
            'upload_id': '1',
            'age':'1',
            'is_cgc_rated':'',
            'cgc_rating':'',
            'label_colour':'',
            'condition_rating':'1',
            'is_canadian_priced_variant':'true',
            'is_variant_cover':'true',
            'is_retail_incentive_variant':'true',
            'is_newsstand_edition':'true',
            'price':'45',
            'cost':'666',
            'section':'1',
            'store':'1',
        },**KWARGS)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'saved',response.content)
        
        # Test
        comic = Comic.objects.all()[0]
        response = client.post('/inventory/1/1/add/comic/1/add_product',{
            'comic_id': str(comic.comic_id),
            'type': 1,
            'upload_id': '1',
            'age':'1',
            'is_cgc_rated':'',
            'cgc_rating':'',
            'label_colour':'',
            'condition_rating':'1',
            'is_canadian_priced_variant':'true',
            'is_variant_cover':'true',
            'is_retail_incentive_variant':'true',
            'is_newsstand_edition':'true',
            'price':'45',
            'cost':'999',
            'section':'1',
            'store':'1',
        },**KWARGS)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'saved',response.content)

        # Verify.
        comic = Comic.objects.all()[0]
        response = client.post('/inventory/1/1/add/comic/1/product/'+str(comic.comic_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Winter World (2015 series)',response.content)
        self.assertIn(b'45',response.content)
        self.assertIn(b'999',response.content)

