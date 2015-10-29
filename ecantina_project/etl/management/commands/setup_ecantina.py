import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ecantina_project import constants
from api.models.ec.category import Category

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
        #-----------------
        # Category
        #-----------------
        try:
            categories = Category.objects.all()
            if len(categories) <= 0:
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
        except Category.DoesNotExist:
            pass

        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "ec_categories", "primarykey": "category_id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('Comics Cantina is now setup!')
