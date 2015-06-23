import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from inventory.views import add
from inventory.models.gcd.issue import Issue
from inventory.models.cc.store import Store
from inventory.models.cc.employee import Employee
from inventory.models.cc.imageupload import ImageUpload


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo@gah.com"
TEST_USER_PASSWORD = "ContinentalUnion"


class AddProductTest(TestCase):
    """
        Run in Console:
        python manage.py test inventory.tests.test_add_product
    """
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()
        Store.objects.all().delete()
        Employee.objects.all().delete()
        uploads = ImageUpload.objects.all()
        for upload in uploads:
            upload.delete()
        issues = Issue.objects.all()
        for issue in issues:
            issue.delete()
    
    def setUp(self):
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()
        store = Store.objects.create(
            store_id=1,
            image ='uploads/bascomics_logo.png',
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
            employee_id=1,
            role=settings.EMPLOYEE_OWNER_ROLE,
            image='',
            store=store,
            user=user,
        )
        Issue.objects.create(
            issue_id=1,
            number=1,
            volume=1,
            no_volume=True,
#            display_volume_with_number = display_volume_with_number,
#            series = series,
#            indicia_publisher = indicia_publisher,
#            indicia_pub_not_printed = indicia_pub_not_printed,
#            brand = brand,
#            no_brand = no_brand,
#            publication_date = publication_date,
#            key_date = key_date,
            sort_code = 1,
#            price = price,
#            page_count = page_count,
#            page_count_uncertain = page_count_uncertain,
#            indicia_frequency = indicia_frequency,
#            no_indicia_frequency = no_indicia_frequency,
#            editing = editing,
#            no_editing = no_editing,
#            notes = notes,
#            created = created,
#            modified = modified,
#            reserved = reserved,
#            deleted = deleted,
#            is_indexed = is_indexed,
#            isbn = isbn,
#            valid_isbn = valid_isbn,
#            no_isbn = no_isbn,
#            variant_of_id = variant_of_id,
#            variant_name = variant_name,
#            barcode = barcode,
#            no_barcode = no_barcode,
#            title = title,
#            no_title = no_title,
#            on_sale_date = on_sale_date,
#            on_sale_date_uncertain = on_sale_date_uncertain,
#            rating = rating,
#            no_rating = no_rating,
        )

    def test_url_resolves_to_add_inventory_search_page_view(self):
        found = resolve('/inventory/add')
        self.assertEqual(found.func, add.add_inventory_search_page)

    def test_url_resolves_to_section_dropbox_page_view(self):
        found = resolve('/inventory/add/1/section_dropbox/1')
        self.assertEqual(found.func, add.sections_per_location)

    def test_url_resolves_to_add_upload_cover_view(self):
        found = resolve('/inventory/add/1/upload_cover')
        self.assertEqual(found.func, add.save_uploaded_cover)

    def test_url_resolves_to_add_product_view(self):
        found = resolve('/inventory/add/1/add_product')
        self.assertEqual(found.func, add.add_product)

    def test_url_resolves_to_list_products_view(self):
        found = resolve('/inventory/add/1/list_products')
        self.assertEqual(found.func, add.list_products)

    def test_add_inventory_search_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Cantina',response.content)

    def test_sections_per_location(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/inventory/add/1/section_dropbox/1', {}, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id_section',response.content)

    def test_upload_cover(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        file_path = settings.MEDIA_ROOT + '/upload/pepe.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/inventory/add/1/upload_cover', {
                'image': fp,
            }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_add_product(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/inventory/add/1/add_product', {
            'upload_id': '',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_sections_per_location(self):
        client = Client()
        client.login(
           username=TEST_USER_USERNAME,
           password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/inventory/add/1/list_products', {}, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.content)
