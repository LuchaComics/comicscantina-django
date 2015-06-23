import os
import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from inventory.models.cc.store import Store
from inventory.models.cc.employee import Employee
from inventory.models.cc.location import Location
from inventory.models.cc.section import Section

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
        
        # Create our Store
        try:
            store = Store.objects.get(store_id=1)
        except Store.DoesNotExist:
            store = Store.objects.create(
            store_id=1,
            image ='upload/bascomics_logo.png',
            name='BA Comic\'s',
            description='Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
            joined=datetime.datetime.now(),
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
        )
        
        # Create our store User(s)
        try:
            user = User.objects.get(username="test@test.com")
        except User.DoesNotExist:
            user = User.objects.create_user(
                'test@test.com',
                'test@test.com',
                '123password',
            )
            user.first_name = 'Smug'
            user.last_name = 'Frog'
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            employee = Employee.objects.create(
                employee_id=1,
                role=settings.EMPLOYEE_OWNER_ROLE,
                image='upload/pepe.png',
                store=store,
                user=user,
            )
        
        # Create Store Location
        locations = Location.objects.filter(store=store)
        main_location = None
        warehouse_location = None
        if len(locations) is 0:
            main_location = Location.objects.create(
                location_id=1,
                name='Main Store',
                store=store,
            )
            warehouse_location = Location.objects.create(
                location_id=3,
                name='Storage Locker',
                store=store,
            )
        
        # Create Sections
        sections = Section.objects.filter(store=store)
        if len(sections) is 0:
            Section.objects.create(
                section_id=1,
                name='Downstairs',
                store=store,
                location=main_location,
            )
            Section.objects.create(
                section_id=2,
                name='Upstairs',
                store=store,
                location=main_location,
            )
            Section.objects.create(
                section_id=3,
                name='Front Pile',
                store=store,
                location=warehouse_location,
            )
            Section.objects.create(
                section_id=4,
                name='Back Pile',
                store=store,
                location=warehouse_location,
            )
        
        #TODO: Impl.
        self.stdout.write('Comics Cantina is now setup!')
