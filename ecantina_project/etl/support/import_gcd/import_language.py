import os
import sys
import xml.sax
from django.conf import settings
from api.models.gcd.language import GCDLanguage

TODO_COMMAND = "TODO_ME_NOW"

class ImportLanguage(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.language_id = None
        self.name = None
        self.code = None
    
    #-----------#
    #  Extract  #
    #-----------#
    def startElement(self, name, attrs):
        if name == 'id':
            self.language_id = TODO_COMMAND
        if name == 'name':
            self.name = TODO_COMMAND
        if name == 'code':
            self.code = TODO_COMMAND

    def characters(self, content):
        if self.language_id is TODO_COMMAND:
            self.language_id = content
        if self.name is TODO_COMMAND:
            self.name = content
        if self.code is TODO_COMMAND:
            self.code = content

    def endElement(self, name):
        if self.code is not None:
            #print(self.language_id + " " + str(self.name) + " " + str(self.code))
            self.import_row(self.language_id, str(self.name), str(self.code))
            self.country_id = None
            self.name = None
            self.code = None
    
    def import_row(self, id, name, code):
        #-----------#
        # Transform #
        #-----------#
        # (Nothing)
        
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