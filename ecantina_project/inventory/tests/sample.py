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
from inventory.models.gcd.country import Country
from inventory.models.gcd.publisher import Publisher
from inventory.models.gcd.language import Language
from inventory.models.gcd.series import Series
from inventory.models.gcd.issue import Issue
from inventory.models.gcd.story import Story
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.location import Location
from inventory.models.ec.section import Section
from django.db import IntegrityError, transaction

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"


class SamplDataPopulator():
    def populate(self):
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self.run_populate()
        except IntegrityError:
            pass
    
    def dealloc(self):
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self.run_dealloc()
        except IntegrityError:
            pass

    def run_dealloc(self):
        for image in ImageUpload.objects.all():
            image.delete()
        for org in Organization.objects.all():
            org.delete()
        for store in Store.objects.all():
            store.delete()
        for employee in Employee.objects.all():
            employee.delete()
        User.objects.all().delete()

    def run_populate(self):
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
                joined = datetime.now(),
                street_name = 'Centre Street',
                street_number = '120',
                unit_number = '102',
                city = 'London',
                province = 'Ontario',
                country = 'Canada',
                postal = 'N6J4X4',
                email = 'bmika@icloud.com',
                phone = '519-432-7898',
                role = settings.EMPLOYEE_OWNER_ROLE,
                user = user,
                organization = organization,
                profile=profile,
            )
        except Exception as e:
            pass

        #-----------
        # Country
        #----------
        country = Country.objects.create(
            country_id=1,
            code='ca',
            name='Canada',
        )

        #------------
        # Language
        #-----------
        language = Language.objects.create(
            language_id=1,
            code='En',
            name='English',
        )

        #-----------------
        # Publisher
        #-----------------
        publisher = Publisher.objects.create(
            publisher_id=1,
            name='Lucha Comics',
            year_began='2015',
#            year_ended=year_ended,
#            notes=notes,
#            url=url,
#            is_master=is_master,
#            # parent_id
#            imprint_count=imprint_count,
#            brand_count=brand_count,
#            indicia_publisher_count=indicia_publisher_count,
#            series_count=series_count,
#            created=created,
#            modified=modified,
#            issue_count=issue_count,
#            reserved=reserved,
#            deleted=deleted,
#            year_began_uncertain=year_began_uncertain,
#            year_ended_uncertain=year_ended_uncertain,
            country=country,
        )

        #-----------------
        # Series
        #-----------------
        series = Series.objects.create(
            series_id=1,
            name='Winter World',
            sort_name='Winter World',
#            format=format,
            year_began='2015',
            year_ended='3000',
#            year_began_uncertain=year_began_uncertain,
#            year_ended_uncertain=year_ended_uncertain,
#            publication_dates=publication_dates,
#            is_current=is_current,
            publisher=publisher,
            country=country,
            language=language,
#            tracking_notes=tracking_notes,
#            notes=notes,
#            publication_notes=publication_notes,
#            has_gallery=has_gallery,
#            open_reserve=open_reserve,
#            issue_count=issue_count,
#            created=created,
#            modified=modified,
#            reserved=reserved,
#            deleted=deleted,
#            has_indicia_frequency=has_indicia_frequency,
#            has_isbn=has_isbn,
#            has_barcode=has_barcode,
#            has_issue_title=has_issue_title,
#            has_volume=has_volume,
#            is_comics_publication=is_comics_publication,
#            color=color,
#            dimensions=dimensions,
#            paper_stock=paper_stock,
#            binding=binding,
#            publishing_format=publishing_format,
#            has_rating=has_rating,
#            publication_type_id=publication_type_id,
#            is_singleton=is_singleton,
        )

        #-----------------
        # Issue
        #-----------------
        Issue.objects.create(
            issue_id=1,
                number='1',
                volume='1',
#                no_volume=False,
#                display_volume_with_number=True,
            series = series,
#                indicia_publisher = None,
#                indicia_pub_not_printed = True,
#                brand = None,
#                no_brand = True,
#                publication_date = 'December 9',
#                                 key_date = key_date,
            sort_code = '0',
#                                 price = price,
#                                 page_count = page_count,
#                                 page_count_uncertain = page_count_uncertain,
#                                 indicia_frequency = indicia_frequency,
#                                 no_indicia_frequency = no_indicia_frequency,
#                                 editing = editing,
#                                 no_editing = no_editing,
#                                 notes = notes,
#                                 created = created,
#                                 modified = modified,
#                                 reserved = reserved,
#                                 deleted = deleted,
#                                 is_indexed = is_indexed,
#                                 isbn = isbn,
#                                 valid_isbn = valid_isbn,
#                                 no_isbn = no_isbn,
#                                 variant_of_id = variant_of_id,
#                                 variant_name = variant_name,
#                                 barcode = barcode,
#                                 no_barcode = no_barcode,
                                 title = 'Winter World',
#                                 no_title = no_title,
#                                 on_sale_date = on_sale_date,
#                                 on_sale_date_uncertain = on_sale_date_uncertain,
#                                 rating = rating,
#                                 no_rating = no_rating,
        )