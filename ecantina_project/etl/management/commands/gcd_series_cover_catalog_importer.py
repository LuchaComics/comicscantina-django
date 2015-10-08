import os
import sys
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models.gcd.series import GCDSeries


LARGE_ZOOM = 4
MEDIUM_ZOOM = 2
SMALL_ZOOM = 1
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2


class GCDSeriesCoverCatalogImporter:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        for event, elem in ET.iterparse(self.file_path):
            if elem.tag == "row":
                self.import_row(elem)
                elem.clear()

    def import_row(self, row):
        id = int(row.findtext('id'))
        url = row.findtext('url')

        print("GCDSeriesCoverCatalogImporter: Updating: " + str(id))
        try:
            series = Series.objects.get(series_id=id)
        except Series.DoesNotExist:
            print("Error: Series "+str(id)+" does not exist.")
            return
        series.cover_url = url
        series.save()

class Command(BaseCommand):
    """
        --------------------------------
        gcd_issue_cover_catalog_importer
        --------------------------------
        
        Run in your console:
        $ python manage.py gcd_series_cover_catalog_importer /Users/bartlomiejmika/Developer/comicscantina/py-comicscantina/scripts/cover/series_catalog.xml
        
        (Where that file path is the path to where the GCD XML files are located)
    """
    help = 'ETL updates our applicaton with the latest series images using the provided xml files.'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+')
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for file_path in options['file_path']:
            importer = GCDSeriesCoverCatalogImporter(full_file_path)
            importer.begin_import()
