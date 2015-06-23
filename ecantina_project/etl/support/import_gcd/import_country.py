import os
import sys
import xml.sax
from django.conf import settings
from inventory.models.gcd.country import Country

TODO_COMMAND = "TODO_ME_NOW"

class ImportCountry(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.country_id = None
        self.name = None
        self.code = None
    
    def startElement(self, name, attrs):
        if name == 'id':
            self.country_id = TODO_COMMAND
        if name == 'name':
            self.name = TODO_COMMAND
        if name == 'code':
            self.code = TODO_COMMAND

    def characters(self, content):
        if self.country_id is TODO_COMMAND:
            self.country_id = content
        if self.name is TODO_COMMAND:
            self.name = content
        if self.code is TODO_COMMAND:
            self.code = content

    def endElement(self, name):
        if self.code is not None:
            #print(self.country_id + " " + str(self.name) + " " + str(self.code))
            self.import_row(self.country_id, str(self.name), str(self.code))
            self.country_id = None
            self.name = None
            self.code = None

    def import_row(self, id, name, code):
        #-----------#
        #  Extract  #
        #-----------#
        
        #-----------#
        # Transform #
        #-----------#
        # (Nothing)
        
        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = Country.objects.get(country_id=id)
            print("ImportCountry: Updating: " + str(id))
            entry.code = code
            entry.name = name
            entry.save()
        except Country.DoesNotExist:
            print("ImportCountry: Inserting: " + str(id))
            Country.objects.create(
                country_id=id,
                code=code,
                name=name,
            ).save()