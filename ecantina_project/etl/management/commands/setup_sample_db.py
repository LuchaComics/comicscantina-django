import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ecantina_project import constants

# Grand Comics Database Models
#------------------------------------------------------------------
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.branduse import GCDBrandUse
from api.models.gcd.brandemblemgroup import GCDBrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from api.models.ec.imagebinaryupload import ImageBinaryUpload
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.imageupload import ImageUpload
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.helprequest import HelpRequest
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.wishlist import Wishlist
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.models.ec.tag import Tag
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from api.models.ec.emailsubscription import EmailSubscription
from api.models.ec.unified_shipping_rates import UnifiedShippingRate
from api.models.ec.print_history import PrintHistory
from api.models.ec.subdomain import SubDomain
from api.models.ec.banned_domain import BannedDomain
from api.models.ec.banned_ip import BannedIP
from api.models.ec.banned_word import BannedWord
from api.models.ec.catalog_item import CatalogItem


class Command(BaseCommand):
    """
        ----------------------
        setup_comicscantina
        ----------------------
        This command will initialize our database.
        
        Run in your console:
        $ python manage.py setup_ecantina
    """
    help = 'Populates the tables neccessary to give us a initial start.'
    
    def handle(self, *args, **options):
        # Defensive Code: Prevent this custom command code from running if
        #                 the application is not in 'Unit Test' mode.
        is_running_unit_tests = len(sys.argv) > 1 and sys.argv[1] == 'test'
        if not is_running_unit_tests:
            self.stdout.write('Cannot run, only acceptable command in unit testing.')
            return
        
        # Get the current time.
        now = datetime.now()
        
        #----------------
        # Administrator
        #----------------
        try:
            user = User.objects.get(email='bmika@icloud.com')
        except User.DoesNotExist:
            user = User.objects.create_user(
                'bmika@icloud.com',  # Username
                'bmika@icloud.com',  # Email
                '123password',
            )
            user.first_name = 'Bart'
            user.last_name = 'Mika'
            user.is_active = True
            user.save()
            user = User.objects.get(email='bmika@icloud.com')

#        #----------------
#        # Image Uploads
#        #----------------
#        try:
#            org_logo = ImageUpload.objects.get(upload_id=1)
#        except ImageUpload.DoesNotExist:
#            org_logo = ImageUpload.objects.create(
#                upload_id = 1,
#                upload_date = now,
#                image = 'upload/bascomics_logo.png',
#                user = user,
#            )
#
#        try:
#            profile = ImageUpload.objects.get(upload_id=2)
#        except ImageUpload.DoesNotExist:
#            profile = ImageUpload.objects.create(
#                upload_id = 2,
#                upload_date = now,
#                image = 'upload/pepe.png',
#                user = user,
#            )
#
#        try:
#            store_logo = ImageUpload.objects.get(upload_id=1)
#        except ImageUpload.DoesNotExist:
#            store_logo = ImageUpload.objects.create(
#                upload_id = 3,
#                upload_date = now,
#                image = 'upload/bascomics_logo.png',
#                user = user,
#            )
        org_logo = None
        profile = None
        store_logo = None

        #-----------------
        # Organization
        #-----------------
        try:
            organization = Organization.objects.get(org_id=1)
        except Organization.DoesNotExist:
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
                phone='5194399636',
                fax=None,
                twitter='bascomics',
                facebook_url=None,
                instagram_url=None,
                linkedin_url=None,
                github_url=None,
                google_url='https://plus.google.com/105760942218297346537/about',
                youtube_url=None,
                flickr_url=None,
                administrator = user,
                logo = org_logo,
                paypal_email = 'rodolfo@theshootingstarpress.com',
            )

        #-----------------
        # Store
        #-----------------
        try:
            store = Store.objects.get(store_id=1)
        except Store.DoesNotExist:
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
                phone='5194399636',
                fax=None,
                organization=organization,
                logo=store_logo,
                is_open_monday = True,
                is_open_tuesday = True,
                is_open_wednesday = True,
                is_open_thursday = True,
                is_open_friday = True,
                is_open_saturday = True,
                is_open_sunday = False,
                monday_to = '18:00',
                tuesday_to = '18:00',
                wednesday_to = '18:00',
                thursday_to = '18:00',
                friday_to = '18:00',
                saturday_to = '18:00',
                sunday_to = '18:00',
                monday_from = '08:00',
                tuesday_from = '08:00',
                wednesday_from = '08:00',
                thursday_from = '08:00',
                friday_from = '08:00',
                saturday_from = '08:00',
                sunday_from = '08:00',
                paypal_email = 'rodolfo@theshootingstarpress.com',
            )

        #-----------------
        # Employees
        #-----------------
        try:
            owner = Employee.objects.get(employee_id=1)
        except Employee.DoesNotExist:
            owner = Employee.objects.create(
                employee_id=1,
                joined = datetime.now(),
                role = constants.EMPLOYEE_OWNER_ROLE,
                user = user,
                organization = organization,
                profile=profile,
            )
            # Make "Owner" an employee of that store.
            store.employees.add(owner)
            store.save()
        
        # Create Sections
        try:
            sections = Section.objects.filter(store=store)
        except Section.DoesNotExist:
            Section.objects.create(
                section_id=1,
                name='Downstairs',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=2,
                name='Upstairs',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=3,
                name='Front Pile',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=4,
                name='Back Pile',
                store=store,
                organization = organization,
            )

        #-----------------
        # Tag
        #-----------------
        try:
            tags = Tag.objects.all()
        except Tag.DoesNotExist:
            Tag.objects.create(
                tag_id=1,
                name = 'Marvel',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=2,
                name = 'DC',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=3,
                name = 'Image',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=4,
                name = 'BOOM!',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=5,
                name = 'Lucha Comics',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=6,
                name = 'Dark Horse',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=7,
                name = 'Dynamite',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=8,
                name = 'IDW',
                organization_id = 1,
            )
            Tag.objects.create(
                tag_id=9,
                name = 'Batman',
                organization_id = 1,
            )

        #-----------------
        # GCD Language
        #-----------------
        try:
            english = GCDLanguage.objects.get(language_id=25)
        except GCDLanguage.DoesNotExist:
            english = GCDLanguage.objects.create(
                language_id=25,
                name = 'English',
                code = 'en',
            )

        #-----------------
        # GCD Country
        #-----------------
        try:
            canada = GCDCountry.objects.get(country_id=36)
            united_states = GCDCountry.objects.get(country_id=225)
        except GCDCountry.DoesNotExist:
            canada = GCDCountry.objects.create(
                country_id=36,
                name = 'Canada',
                code = 'en',
            )
            united_states = GCDCountry.objects.create(
                country_id=225,
                name = 'United States',
                code = 'us',
            )

        #-----------------
        # GCD Publisher
        #-----------------
        try:
            marvel = GCDPublisher.objects.get(publisher_id=500)
        except GCDPublisher.DoesNotExist:
            marvel = GCDPublisher.objects.create(
                publisher_id=666,
                name = 'Marvel',
                year_began = 2000,
                year_ended = 2016,
                notes = "",
                url = "http://www.comicscantina.com",
                country = canada,
            )

        #-----------------
        # GCD Series
        #-----------------
        try:
            series = GCDSeries.objects.get(publisher_id=500)
        except GCDSeries.DoesNotExist:
            series = GCDSeries.objects.create(
                series_id=666,
                name = 'Winterworld',
                sort_name = 'Winterworld',
                year_began = 2000,
                year_ended = 2016,
                publication_dates = "2014-01-01",
                country = canada,
                language = english,
                publisher = marvel,
                publisher_name = "Marvel",
            )

        #------------
        #TODO: Continue adding here ...
        
        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "ec_brands", "primarykey": "brand_id",},
            {"tablename": "ec_comics", "primarykey": "comic_id",},
            {"tablename": "ec_customers", "primarykey": "customer_id",},
            {"tablename": "ec_employees", "primarykey": "employee_id",},
#            {"tablename": "ec_email_subscriptions", "primarykey": "subscription_id",},
            {"tablename": "ec_help_requests", "primarykey": "help_id",},
            {"tablename": "ec_image_uploads", "primarykey": "upload_id",},
            {"tablename": "ec_org_shipping_preferences", "primarykey": "shipping_pref_id",},
            {"tablename": "ec_org_shipping_rates", "primarykey": "shipping_rate_id",},
            {"tablename": "ec_organizations", "primarykey": "org_id",},
            {"tablename": "ec_products", "primarykey": "product_id",},
            {"tablename": "ec_promotions", "primarykey": "promotion_id",},
            {"tablename": "ec_pulllists", "primarykey": "pulllist_id",},
            {"tablename": "ec_pulllists_subscriptions", "primarykey": "subscription_id",},
            {"tablename": "ec_receipts", "primarykey": "receipt_id",},
            {"tablename": "ec_sections", "primarykey": "section_id",},
            {"tablename": "ec_stores", "primarykey": "store_id",},
            {"tablename": "ec_store_shipping_preferences", "primarykey": "shipping_pref_id",},
            {"tablename": "ec_store_shipping_rates", "primarykey": "shipping_rate_id",},
            {"tablename": "ec_tags", "primarykey": "tag_id",},
            {"tablename": "ec_wishlists", "primarykey": "wishlist_id",},
            # Grand Comics Database Tables
            {"tablename": "gcd_brands", "primarykey": "brand_id",},
            {"tablename": "gcd_brand_emblem_groups", "primarykey": "brand_emblem_group_id",},
            {"tablename": "gcd_brand_groups", "primarykey": "brand_group_id",},
            {"tablename": "gcd_brand_uses", "primarykey": "brand_use_id",},
            {"tablename": "gcd_countries", "primarykey": "country_id",},
            {"tablename": "gcd_images", "primarykey": "image_id",},
            {"tablename": "gcd_indicia_publishers", "primarykey": "indicia_publisher_id",},
            {"tablename": "gcd_issues", "primarykey": "issue_id",},
            {"tablename": "gcd_languages", "primarykey": "language_id",},
            {"tablename": "gcd_publishers", "primarykey": "publisher_id",},
            {"tablename": "gcd_series", "primarykey": "series_id",},
            {"tablename": "gcd_stories", "primarykey": "story_id",},
            {"tablename": "gcd_story_types", "primarykey": "story_type_id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)