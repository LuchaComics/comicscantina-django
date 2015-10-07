import os
import sys
import xml.sax
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models.gcd.series import GCDSeries


LARGE_ZOOM = 4
MEDIUM_ZOOM = 2
SMALL_ZOOM = 1
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2


class GCDSeriesCoverCatalogImporter(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.found_series = False

    def import_from_attrs(self, attrs):
        id = int(attrs.getValue("id"))
        url = attrs.getValue("url")
        print("GCDSeriesCoverCatalogImporter: Updating: " + str(id))
        try:
            series = Series.objects.get(series_id=id)
        except Series.DoesNotExist:
            print("Error: Series "+str(id)+" does not exist.")
            return
        series.cover_url = url
        series.save()

    def startElement(self, name, attrs):
        if name == 'series':
            self.import_from_attrs(attrs)

    def characters(self, content):
        pass

    def endElement(self, name):
        pass

class Command(BaseCommand):
    """
        ----------------------
        import_gcd_covers
        ----------------------
        ETL will load up the catalog.xml file for the Series Cover assets and
        update the associated Series in the database to reference the imported
        covers.
        
        Run in your console:
        $ python manage.py import_gcd_series_covers /Users/bartlomiejmika/Developer/comicscantina/py-comicscantina/scripts/cover/series_catalog.xml
        
        (Where that file path is the path to where the GCD XML files are located)
    """
    help = 'ETL loads up the GCD database into our applicaton using the provided xml files.'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+')
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for file_path in options['file_path']:
            print(file_path)
            source = open(file_path)
            xml.sax.parse(source, GCDSeriesCoverCatalogImporter())
