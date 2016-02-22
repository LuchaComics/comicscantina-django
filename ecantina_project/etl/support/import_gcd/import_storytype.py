import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.storytype import GCDStoryType


class ImportStoryType:
    """
        Class is responsible for opening XML file and importing into database.
    """
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        # Remove the text formating.
        # http://stackoverflow.com/questions/15977075/elementtree-parseerror-not-well-formed-invalid-token
        fp = self.file_path
        os.system("tr -dc '[\011\012\015\040-\176\200-\377]' < "+fp+" > "+fp+"2;")
        os.system("mv "+fp+"2 "+fp+";")
        
        # Iterate through the contents of the file and import it.
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
        sort_code = row.findtext('sort_code')

        #-----------#
        # Transform #
        #-----------#
    
        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDStoryType.objects.get(story_type_id=id)
            print("ImportStoryType: Updating: " + str(id))
            entry.name = name
            entry.sort_code = sort_code
            entry.save()
        except GCDStoryType.DoesNotExist:
            print("ImportStoryType: Inserting: " + str(id))
            GCDStoryType.objects.create(
                story_type_id=id,
                name=name,
                sort_code=sort_code,
            )