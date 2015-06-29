import os
import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.location import Location
from inventory.models.ec.section import Section

class Command(BaseCommand):
    """
        ----------------------
        setup_comicscantina
        ----------------------
        This command will initialize our database.
        
        Run in your console:
        $ python manage.py setup_comicscantina
    """
    help = 'Populates the tables neccessary to give us a initial start.'
    
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        now = datetime.datetime.now()
        
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
            logo = ImageUpload.objects.create(
                upload_id = 1,
                upload_date = now,
                image = 'upload/bascomics_logo.png',
                user = user,
            )
        except Exception as e:
            logo = ImageUpload.objects.get(upload_id=1)
        try:
            profile = ImageUpload.objects.create(
                upload_id = 2,
                upload_date = now,
                image = 'upload/pepe.png',
                user = user,
            )
        except Exception as e:
            profile = ImageUpload.objects.get(upload_id=2)

        #-----------------
        # Organization
        #-----------------
        try:
            organization = Organization.objects.create(
                org_id=1,
                name='BA Comic\'s',
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
        
        # Create Store Location
        locations = Location.objects.filter(store=store)
        main_location = None
        warehouse_location = None
        if len(locations) is 0:
            main_location = Location.objects.create(
                location_id=1,
                name='Main Store',
                store=store,
                organization = organization,
            )
            warehouse_location = Location.objects.create(
                location_id=3,
                name='Storage Locker',
                store=store,
                organization = organization,
            )
        
        # Create Sections
        sections = Section.objects.filter(store=store)
        if len(sections) is 0:
            Section.objects.create(
                section_id=1,
                name='Downstairs',
                store=store,
                location=main_location,
                organization = organization,
            )
            Section.objects.create(
                section_id=2,
                name='Upstairs',
                store=store,
                location=main_location,
                organization = organization,
            )
            Section.objects.create(
                section_id=3,
                name='Front Pile',
                store=store,
                location=warehouse_location,
                organization = organization,
            )
            Section.objects.create(
                section_id=4,
                name='Back Pile',
                store=store,
                location=warehouse_location,
                organization = organization,
            )

        #------------
        #TODO: Continue adding here ...
        
        
        self.stdout.write('Comics Cantina is now setup!')
