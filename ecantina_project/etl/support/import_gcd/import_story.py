import os
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.conf import settings
from api.models.gcd.storytype import StoryType
from api.models.gcd.story import Story
from api.models.gcd.issue import Issue

class ImportStory:
    """
        Class is responsible for opening CSV file and importing into database.
        
        HOWTO: Setup File for processing.
        Step (1):
        Go to the directory where our publisher file exists and run this:
        tr -dc '[\011\012\015\040-\176\200-\377]' < gcd_story.xml > gcd_story2.xml
        
        Step (2):
        Rename gcd_story_type2 to gcd_story_type and delete old.
        mv gcd_story2.xml gcd_story.xml
        
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
        title = row.findtext('title')
        title_inferred = row.findtext('title_inferred')
        feature = row.findtext('feature')
        sequence_number = row.findtext('sequence_number')
        page_count = row.findtext('page_count')
        issue_id = row.findtext('issue_id')
        script = row.findtext('script')
        pencils = row.findtext('pencils')
        inks = row.findtext('inks')
        colors = row.findtext('colors')
        letters = row.findtext('letters')
        editing = row.findtext('editing')
        genre = row.findtext('genre')
        characters = row.findtext('characters')
        synopsis = row.findtext('synopsis')
        reprint_notes = row.findtext('reprint_notes')
        created = row.findtext('created')
        modified = row.findtext('modified')
        notes = row.findtext('notes')
        no_script = row.findtext('no_script')
        no_pencils = row.findtext('no_pencils')
        no_inks = row.findtext('no_inks')
        no_colors = row.findtext('no_colors')
        no_letters = row.findtext('no_letters')
        no_editing = row.findtext('no_editing')
        page_count_uncertain = row.findtext('page_count_uncertain')
        type_id = row.findtext('type_id')
        job_number = row.findtext('job_number')
        name = row.findtext('name')
        reserved = row.findtext('reserved')
        deleted = row.findtext('deleted')

        #-----------#
        # Transform #
        #-----------#
        page_count = 0 if page_count in 'NULL' else Decimal(page_count)

        try:
            story_type = StoryType.objects.get(story_type_id = type_id)
        except StoryType.DoesNotExist:
            story_type = None

        try:
            issue = Issue.objects.get(issue_id = issue_id)
        except Issue.DoesNotExist:
            issue = None

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = Story.objects.get(story_id=id)
            print("ImportStory: Updating: " + str(id))
            entry.save()
        except Story.DoesNotExist:
            print("ImportStory: Inserting: " + str(id))
            Story.objects.create(
                story_id=id,
                title = title,
                title_inferred = title_inferred,
                feature = feature,
                sequence_number = sequence_number,
                page_count = page_count,
                issue = issue,
                script = script,
                pencils = pencils,
                inks = inks,
                colors = colors,
                letters = letters,
                editing = editing,
                genre = genre,
                characters = characters,
                synopsis = synopsis,
                reprint_notes = reprint_notes,
                created = created,
                modified = modified,
                notes = notes,
                no_script = no_script,
                no_pencils = no_pencils,
                no_inks = no_inks,
                no_colors = no_colors,
                no_letters = no_letters,
                no_editing = no_editing,
                page_count_uncertain = page_count_uncertain,
                type = story_type,
                job_number = job_number,
                reserved = reserved,
                deleted = deleted,
            )