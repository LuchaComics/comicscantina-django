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

        #------------
        #TODO: Continue adding here ...
        
        
        self.stdout.write('Comics Cantina is now setup!')
