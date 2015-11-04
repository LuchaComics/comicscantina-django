import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.country import GCDCountry


class ImportCountry:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        for event, elem in ET.iterparse(self.file_path):
            if elem.tag == "row":
                self.import_row(elem)
                elem.clear()

    def import_row(self, row):
        #-----------#
        #  Extract  #
        #-----------#
        id = int(row.findtext('id'))
        name = row.findtext('name')
        code = row.findtext('code')

        #-----------#
        # Transform #
        #-----------#
        # Do nothing...

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDCountry.objects.get(country_id=id)
            print("ImportCountry: Updating: " + str(id))
            entry.code = code
            entry.name = name
            entry.save()
        except GCDCountry.DoesNotExist:
            print("ImportCountry: Inserting: " + str(id))
            GCDCountry.objects.create(
                country_id=id,
                code=code,
                name=name,
            ).save()
