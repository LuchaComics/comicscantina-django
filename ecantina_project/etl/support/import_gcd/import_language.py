import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.language import GCDLanguage


class ImportLanguage:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        # Remove the text formating.
        fp = self.file_path
        os.system("tr -dc '[\011\012\015\040-\176\200-\377]' < "+fp+" > "+fp+"2;")
        os.system("mv "+fp+"2 "+fp+";")
        
        # Iterate through the contents of the file and import it.
        for event, elem in ET.iterparse(self.file_path):
            if elem.tag == "row":
                self.import_row(elem)
                elem.clear()

    def import_row(self, root):
        #-----------#
        #  Extract  #
        #-----------#
        id = 0
        name = None
        code = None
        for child in root:
            if child.attrib['name'] == 'id':
                id = child.text
            if child.attrib['name'] == 'name':
                name = child.text
            if child.attrib['name'] == 'code':
                code = child.text
        
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