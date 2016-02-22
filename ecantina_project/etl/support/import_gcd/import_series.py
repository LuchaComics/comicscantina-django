import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.series import GCDSeries


class ImportSeries:
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
        id = int(row.findtext('id'))
        name = row.findtext('name')
        sort_name = row.findtext('sort_name')
        format = row.findtext('format')
        year_began = row.findtext('year_began')
        year_ended = row.findtext('year_ended')
        year_began_uncertain = row.findtext('year_began_uncertain')
        year_ended_uncertain = row.findtext('year_ended_uncertain')
        publication_dates = row.findtext('publication_dates')
        first_issue_id = row.findtext('first_issue_id')
        last_issue_id = row.findtext('last_issue_id')
        is_current = row.findtext('is_current')
        publisher_id = int(row.findtext('publisher_id'))
        country_id = int(row.findtext('country_id'))
        language_id = int(row.findtext('language_id'))
        tracking_notes = row.findtext('tracking_notes')
        notes = row.findtext('notes')
        publication_notes = row.findtext('publication_notes')
        has_gallery = row.findtext('has_gallery')
        open_reserve = row.findtext('open_reserve')
        issue_count = int(row.findtext('issue_count'))
        created = row.findtext('created')
        modified = row.findtext('modified')
        reserved = row.findtext('reserved')
        deleted = row.findtext('deleted')
        has_indicia_frequency = row.findtext('has_indicia_frequency')
        has_isbn = row.findtext('has_isbn')
        has_barcode = row.findtext('has_barcode')
        has_issue_title = row.findtext('has_issue_title')
        has_volume = row.findtext('has_volume')
        is_comics_publication = row.findtext('is_comics_publication')
        color = row.findtext('color')
        dimensions = row.findtext('dimensions')
        paper_stock = row.findtext('paper_stock')
        binding = row.findtext('binding')
        publishing_format = row.findtext('publishing_format')
        has_rating = row.findtext('has_rating')
        publication_type_id = row.findtext('publication_type_id')
        is_singleton = row.findtext('is_singleton')

        #-----------#
        # Transform #
        #-----------#
        try:
            country = GCDCountry.objects.get(country_id=country_id)
        except GCDCountry.DoesNotExist:
            country = None

        try:
            publisher = GCDPublisher.objects.get(publisher_id=publisher_id)
        except GCDPublisher.DoesNotExist:
            publisher = None
        publisher_name = publisher.name
        
        try:
            language = GCDLanguage.objects.get(language_id=language_id)
        except language.DoesNotExist:
            language = None

        # Fix their weird data
        year_began = 0 if year_began in 'NULL' else int(year_began)
        year_began = year_began if year_began <= 9999 else 0
        year_ended = 0 if year_ended in 'NULL' else int(year_ended)
        year_ended = year_ended if year_ended <= 9999 else 0
        year_began_uncertain = False if year_began_uncertain is '0' else True
        year_ended_uncertain = False if year_ended_uncertain is '0' else True
        has_barcode = False if has_barcode is '0' else True
        has_indicia_frequency = False if has_indicia_frequency is '0' else True
        has_isbn = False if has_isbn is '0' else True
        has_issue_title = False if has_issue_title is '0' else True
        has_volume = False if has_volume is '0' else True
        has_rating = False if has_rating is '0' else True
        is_current = False if is_current is '0' else True
        is_comics_publication = False if is_comics_publication is 'NULL' else True
        is_singleton = False if is_singleton is '0' else True
        has_gallery = False if has_gallery is '0' else True
        reserved = False if reserved is '0' else True
        deleted = False if deleted is '0' else True
        first_issue_id = 0 if first_issue_id in 'NULL' else int(first_issue_id)
        last_issue_id = 0 if last_issue_id in 'NULL' else int(last_issue_id)
        publication_type_id = 0 if publication_type_id in 'NULL' else int(publication_type_id)
        open_reserve = 0 if open_reserve in 'NULL' else int(open_reserve)

        # Generate Image URL
        base_url = settings.COMICS_CANTINA_IMAGE_SERVER_BASE_URL + str(id)
        cover_url = base_url + '.jpg'

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDSeries.objects.get(series_id=id)
            print("ImportSeries: Updating: " + str(id))
            entry.name=name
            entry.sort_name=sort_name
            entry.format=format
            entry.year_began=year_began
            entry.year_ended=year_ended
            entry.year_began_uncertain=year_began_uncertain
            entry.year_ended_uncertain=year_ended_uncertain
            entry.publication_dates=publication_dates
            entry.is_current=is_current
            entry.publisher=publisher
            entry.country=country
            entry.language=language
            entry.tracking_notes=tracking_notes
            entry.notes=notes
            entry.publication_notes=publication_notes
            entry.has_gallery=has_gallery
            entry.open_reserve=open_reserve
            entry.issue_count=issue_count
            entry.created=created
            entry.modified=modified
            entry.reserved=reserved
            entry.deleted=deleted
            entry.has_indicia_frequency=has_indicia_frequency
            entry.has_isbn=has_isbn
            entry.has_barcode=has_barcode
            entry.has_issue_title=has_issue_title
            entry.has_volume=has_volume
            entry.is_comics_publication=is_comics_publication
            entry.color=color
            entry.dimensions=dimensions
            entry.paper_stock=paper_stock
            entry.binding=binding
            entry.publishing_format=publishing_format
            entry.has_rating=has_rating
            entry.publication_type_id=publication_type_id
            entry.is_singleton=is_singleton
            entry.publisher_name = publisher_name
            entry.cover_url = cover_url
            entry.save()
        except GCDSeries.DoesNotExist:
            print("ImportSeries: Inserting: " + str(id))
            GCDSeries.objects.create(
                series_id=id,
                name=name,
                sort_name=sort_name,
                format=format,
                year_began=year_began,
                year_ended=year_ended,
                year_began_uncertain=year_began_uncertain,
                year_ended_uncertain=year_ended_uncertain,
                publication_dates=publication_dates,
                is_current=is_current,
                publisher=publisher,
                country=country,
                language=language,
                tracking_notes=tracking_notes,
                notes=notes,
                publication_notes=publication_notes,
                has_gallery=has_gallery,
                open_reserve=open_reserve,
                issue_count=issue_count,
                created=created,
                modified=modified,
                reserved=reserved,
                deleted=deleted,
                has_indicia_frequency=has_indicia_frequency,
                has_isbn=has_isbn,
                has_barcode=has_barcode,
                has_issue_title=has_issue_title,
                has_volume=has_volume,
                is_comics_publication=is_comics_publication,
                color=color,
                dimensions=dimensions,
                paper_stock=paper_stock,
                binding=binding,
                publishing_format=publishing_format,
                has_rating=has_rating,
                publication_type_id=publication_type_id,
                is_singleton=is_singleton,
                publisher_name=publisher_name,
                cover_url=cover_url,
            )