import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.storytype import StoryType


class ImportStoryType:
    """
        Class is responsible for opening CSV file and importing into database.
        
        HOWTO: Setup File for processing.
        Step (1):
            Go to the directory where our publisher file exists and run this:
            tr -dc '[\011\012\015\040-\176\200-\377]' < gcd_story_type.xml > gcd_story_type2.xml
            
        Step (2):
            Rename gcd_story_type2 to gcd_story_type and delete old.
            mv gcd_story_type2.xml gcd_story_type.xml
            
        Step (3):
            This class will work without error.
            
        Note:
            http://stackoverflow.com/questions/15977075/elementtree-parseerror-not-well-formed-invalid-token
    """
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
        sort_code = row.findtext('sort_code')

        #-----------#
        # Transform #
        #-----------#
    
        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = StoryType.objects.get(story_type_id=id)
            print("ImportStoryType: Updating: " + str(id))
            entry.name = name
            entry.sort_code = sort_code
            entry.save()
        except StoryType.DoesNotExist:
            print("ImportStoryType: Inserting: " + str(id))
            StoryType.objects.create(
                story_type_id=id,
                name=name,
                sort_code=sort_code,
            )