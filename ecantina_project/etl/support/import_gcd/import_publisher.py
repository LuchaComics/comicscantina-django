import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.country import GCDCountry
from api.models.gcd.publisher import GCDPublisher


class ImportPublisher:
    """
        Class is responsible for opening CSV file and importing into database.
    """
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
        country_id = None
        year_began = None
        year_ended = None
        notes = None
        url = None
        is_master = None
        parent_id = None
        imprint_count = None
        brand_count = None
        indicia_publisher_count = None
        series_count = None
        created = None
        modified = None
        issue_count = None
        reserved = None
        deleted = None
        year_began_uncertain = 0
        year_ended_uncertain = 0
        for child in root:
            if child.attrib['name'] == 'id':
                id = int(child.text)
            
            if child.attrib['name'] == 'name':
                name = child.text
            
            if child.attrib['name'] == 'country_id':
                country_id = int(child.text)
            
            if child.attrib['name'] == 'year_began':
                year_began = child.text
            
            if child.attrib['name'] == 'year_ended':
                year_ended = child.text
            
            if child.attrib['name'] == 'notes':
                notes = child.text
            
            if child.attrib['name'] == 'url':
                url = child.text
            
            if child.attrib['name'] == 'is_master':
                is_master = child.text
            
            if child.attrib['name'] == 'parent_id':
                parent_id = child.text
            
            if child.attrib['name'] == 'imprint_count':
                imprint_count = child.text
            
            if child.attrib['name'] == 'brand_count':
                brand_count = child.text
            
            if child.attrib['name'] == 'indicia_publisher_count':
                indicia_publisher_count = child.text
            
            if child.attrib['name'] == 'series_count':
                series_count = child.text
            
            if child.attrib['name'] == 'created':
                created = child.text
            
            if child.attrib['name'] == 'modified':
                modified = child.text
            
            if child.attrib['name'] == 'issue_count':
                issue_count = child.text
            
            if child.attrib['name'] == 'reserved':
                reserved = child.text
            
            if child.attrib['name'] == 'deleted':
                deleted = child.text
            
            if child.attrib['name'] == 'year_began_uncertain':
                year_began_uncertain = child.text
            
            if child.attrib['name'] == 'year_ended_uncertain':
                year_ended_uncertain = child.text

        #-----------#
        # Transform #
        #-----------#
        try:
            country = GCDCountry.objects.get(country_id=country_id)
        except GCDCountry.DoesNotExist:
            country = None
    
        # Fix their weird data
        if year_began:
            year_began = 0 if year_began in 'NULL' else int(year_began)
            year_began = year_began if year_began <= 9999 else 0

        if year_ended:
            year_ended = 0 if year_ended in 'NULL' else int(year_ended)
            year_ended = year_ended if year_ended <= 9999 else 0

        # Fix NULL entries into the name.
        if not name:
            name = ""

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDPublisher.objects.get(publisher_id=id)
            print("ImportPublisher: Updating: " + str(id))
            entry.name = name
            entry.year_began = year_began
            entry.year_ended = year_ended
            entry.notes = notes
            entry.url = url
            entry.is_master = is_master
            # entry.parent_id
            entry.imprint_count = imprint_count
            entry.brand_count = brand_count
            entry.indicia_publisher_count = indicia_publisher_count
            entry.series_count= series_count
            entry.created = created
            entry.modified = modified
            entry.issue_count = issue_count
            entry.reserved = reserved
            entry.deleted = deleted
            entry.year_began_uncertain = year_began_uncertain
            entry.year_ended_uncertain = year_ended_uncertain
            entry.country = country
            entry.save()
        except GCDPublisher.DoesNotExist:
            print("ImportPublisher: Inserting: " + str(id))
            GCDPublisher.objects.create(
                publisher_id=id,
                name=name,
                year_began=year_began,
                year_ended=year_ended,
                notes=notes,
                url=url,
                is_master=is_master,
                # parent_id
                imprint_count=imprint_count,
                brand_count=brand_count,
                indicia_publisher_count=indicia_publisher_count,
                series_count=series_count,
                created=created,
                modified=modified,
                issue_count=issue_count,
                reserved=reserved,
                deleted=deleted,
                year_began_uncertain=year_began_uncertain,
                year_ended_uncertain=year_ended_uncertain,
                country=country,
            )