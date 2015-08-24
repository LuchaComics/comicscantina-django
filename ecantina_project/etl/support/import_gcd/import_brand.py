import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.country import GCDCountry
from api.models.gcd.publisher import Publisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand

class ImportBrand:
    """
        Class is responsible for opening CSV file and importing into database.
        
        HOWTO: Setup File for processing.
        Step (1):
            Go to the directory where our publisher file exists and run this:
            tr -dc '[\011\012\015\040-\176\200-\377]' < gcd_brand.xml > gcd_brand2.xml
            
        Step (2):
            Rename gcd_publisher2 to gcd_publisher and delete old.
            mv gcd_brand2.xml gcd_brand.xml
            
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
        parent_id = row.findtext('parent_id')
        year_began = row.findtext('year_began')
        year_ended = row.findtext('year_ended')
        notes = row.findtext('notes')
        url = row.findtext('url')
        created = row.findtext('created')
        modified = row.findtext('modified')
        issue_count = row.findtext('issue_count')
        reserved = row.findtext('reserved')
        deleted = row.findtext('deleted')
        year_began_uncertain = row.findtext('year_began_uncertain')
        year_ended_uncertain = row.findtext('year_ended_uncertain')

        #-----------#
        # Transform #
        #-----------#
        # Fix their weird data
        year_began = 0 if year_began in 'NULL' else int(year_began)
        year_began = year_began if year_began <= 9999 else 0
        year_ended = 0 if year_ended in 'NULL' else int(year_ended)
        year_ended = year_ended if year_ended <= 9999 else 0
        parent_id = 0 if parent_id in 'NULL' else int(parent_id)

        try:
            publisher = Publisher.objects.get(publisher_id=parent_id)
        except Publisher.DoesNotExist:
            publisher = None

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDBrand.objects.get(brand_id=id)
            print("ImportBrand: Updating: " + str(id))
            entry.name = name
            entry.year_began = year_began
            entry.year_ended = year_ended
            entry.notes = notes
            entry.url = url
            entry.created = created
            entry.modified = modified
            entry.issue_count = issue_count
            entry.reserved = reserved
            entry.deleted = deleted
            entry.year_began_uncertain = year_began_uncertain
            entry.year_ended_uncertain = year_ended_uncertain
            entry.parent = publisher
            entry.save()
        except GCDBrand.DoesNotExist:
            print("ImportBrand: Inserting: " + str(id))
            GCDBrand.objects.create(
                brand_id=id,
                name=name,
                year_began=year_began,
                year_ended=year_ended,
                notes=notes,
                url=url,
                created=created,
                modified=modified,
                issue_count=issue_count,
                reserved=reserved,
                deleted=deleted,
                year_began_uncertain=year_began_uncertain,
                year_ended_uncertain=year_ended_uncertain,
                parent=publisher,
            )