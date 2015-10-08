import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.language import GCDLanguage


class ImportLanguage:
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
            entry = GCDLanguage.objects.get(language_id=id)
            print("ImportLanguage: Updating: " + str(id))
            entry.code = code
            entry.name = name
            entry.save()
        except GCDLanguage.DoesNotExist:
            print("ImportLanguage: Inserting: " + str(id))
            GCDLanguage.objects.create(
                language_id=id,
                code=code,
                name=name,
            ).save()