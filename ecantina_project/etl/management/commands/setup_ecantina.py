import os
import sys
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.category import Category
from api.models.ec.tag import Tag

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
        os.system('clear;')  # Clear the console text.
        now = datetime.now()
        
        #----------------
        # Administrator
        #----------------
        try:
            user = User.objects.create_user(
                'bmika@icloud.com',  # Username
                'bmika@icloud.com',  # Email
                '123password',
            )
            user.first_name = 'Bart'
            user.last_name = 'Mika'
            user.is_active = True
            user.save()
        except Exception as e:
            user = User.objects.get(email='bmika@icloud.com')

        #----------------
        # Image Uploads
        #----------------
        try:
            org_logo = ImageUpload.objects.create(
                upload_id = 1,
                upload_date = now,
                image = 'upload/bascomics_logo.png',
                user = user,
            )
        except Exception as e:
            org_logo = ImageUpload.objects.get(upload_id=1)
        try:
            profile = ImageUpload.objects.create(
                upload_id = 2,
                upload_date = now,
                image = 'upload/pepe.png',
                user = user,
            )
        except Exception as e:
            profile = ImageUpload.objects.get(upload_id=2)
        try:
            store_logo = ImageUpload.objects.create(
                upload_id = 3,
                upload_date = now,
                image = 'upload/bascomics_logo.png',
                user = user,
            )
        except Exception as e:
            store_logo = ImageUpload.objects.get(upload_id=1)


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
                logo = org_logo,
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
        
        # Create Sections
        sections = Section.objects.filter(store=store)
        if len(sections) is 0:
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
        # Category
        #-----------------
        try:
            Category.objects.create(
                category_id=1,
                parent_id = 0,
                name = 'Comic',
            )
            Category.objects.create(
                category_id=2,
                parent_id = 1,
                name = 'Comic - Graphic Novel',
            )
            Category.objects.create(
                category_id=3,
                parent_id = 1,
                name = 'Comic - Golden Age',
            )
            Category.objects.create(
                category_id=4,
                parent_id = 1,
                name = 'Comic - Silver Age',
            )
            Category.objects.create(
                category_id=5,
                parent_id = 1,
                name = 'Comic - Bronze Age',
            )
            Category.objects.create(
                category_id=6,
                parent_id = 1,
                name = 'Comic - Modern',
            )
            Category.objects.create(
                category_id=7,
                parent_id = 1,
                name = 'Comic - Trade Paperbacks',
            )
        except Exception as e:
            pass


        #-----------------
        # Tag
        #-----------------
        try:
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
        except Exception as e:
            pass

        #------------
        #TODO: Continue adding here ...
        
        
        self.stdout.write('Comics Cantina is now setup!')
