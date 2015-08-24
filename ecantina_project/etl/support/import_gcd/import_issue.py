import os
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.conf import settings
from api.models.gcd.country import Country
from api.models.gcd.language import Language
from api.models.gcd.publisher import Publisher
from api.models.gcd.indiciapublisher import IndiciaPublisher
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue


class ImportIssue:
    """
        Class is responsible for opening CSV file and importing into database.
        
        HOWTO: Setup File for processing.
        Step (1):
            Go to the directory where our publisher file exists and run this:
            tr -dc '[\011\012\015\040-\176\200-\377]' < gcd_issue.xml > gcd_issue2.xml
            
        Step (2):
            Rename gcd_publisher2 to gcd_publisher and delete old.
            mv gcd_issue2.xml gcd_issue.xml
            
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
        number = row.findtext('number')
        volume = row.findtext('volume')
        no_volume = row.findtext('no_volume')
        display_volume_with_number = row.findtext('display_volume_with_number')
        series_id = row.findtext('series_id')
        indicia_publisher_id = row.findtext('indicia_publisher_id')
        indicia_pub_not_printed = row.findtext('indicia_pub_not_printed')
        brand_id = row.findtext('brand_id')
        no_brand = row.findtext('no_brand')
        publication_date = row.findtext('publication_date')
        key_date = row.findtext('key_date')
        sort_code = row.findtext('sort_code')
        price = row.findtext('price')
        page_count = row.findtext('page_count')
        page_count_uncertain = row.findtext('page_count_uncertain')
        indicia_frequency = row.findtext('indicia_frequency')
        no_indicia_frequency = row.findtext('no_indicia_frequency')
        editing = row.findtext('editing')
        no_editing = row.findtext('no_editing')
        notes = row.findtext('notes')
        created = row.findtext('created')
        modified = row.findtext('modified')
        reserved = row.findtext('reserved')
        deleted = row.findtext('deleted')
        is_indexed = row.findtext('is_indexed')
        isbn = row.findtext('isbn')
        valid_isbn = row.findtext('valid_isbn')
        no_isbn = row.findtext('no_isbn')
        variant_of_id = row.findtext('variant_of_id')
        variant_name = row.findtext('variant_name')
        barcode = row.findtext('barcode')
        no_barcode = row.findtext('no_barcode')
        title = row.findtext('title')
        no_title = row.findtext('no_title')
        on_sale_date = row.findtext('on_sale_date')
        on_sale_date_uncertain = row.findtext('on_sale_date_uncertain')
        rating = row.findtext('rating')
        no_rating = row.findtext('no_rating')

        #-----------#
        # Transform #
        #-----------#
        if brand_id is None:
            brand_id = 0
        else:
            brand_id = 0 if brand_id in 'NULL' else int(brand_id)
        series_id = 0 if series_id in 'NULL' else int(series_id)
        indicia_publisher_id = 0 if indicia_publisher_id in 'NULL' else int(indicia_publisher_id)
        no_title = True if no_title is '1' else False
        no_volume = True if no_volume is '1' else False
        display_volume_with_number = True if display_volume_with_number is '1' else False
        no_isbn = True if no_isbn is '1' else False
        variant_of_id = 0 if variant_of_id in 'NULL' else int(variant_of_id)
        no_barcode = True if no_barcode is '1' else False
        on_sale_date_uncertain = True if on_sale_date_uncertain is '1' else False
        no_rating = True if no_rating is '1' else False
        no_indicia_frequency = True if no_indicia_frequency is '1' else False
        page_count = 0 if page_count in 'NULL' else Decimal(page_count)
        no_editing = True if no_editing in '1' else False
        reserved = True if reserved in '1' else False
        indicia_pub_not_printed = True if indicia_pub_not_printed in '1' else False
        no_brand = True if no_brand in '1' else False
        deleted = True if deleted in '1' else False
        is_indexed = False if is_indexed in 'NULL' else int(is_indexed)

        try:
            indicia_publisher = IndiciaPublisher.objects.get(indicia_publisher_id=indicia_publisher_id)
        except IndiciaPublisher.DoesNotExist:
            indicia_publisher = None
        publisher_name = indicia_publisher.name

        try:
            series = Series.objects.get(series_id=series_id)
        except Series.DoesNotExist:
            series = None
        
        try:
            brand = GCDBrand.objects.get(brand_id=brand_id)
        except GCDBrand.DoesNotExist:
            brand = None


        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = Issue.objects.get(issue_id=id)
            print("ImportIssue: Updating: " + str(id))
            entry.number = number
            entry.volume = volume
            entry.no_volume = no_volume
            entry.display_volume_with_number = display_volume_with_number
            entry.series = series
            entry.indicia_publisher = indicia_publisher
            entry.indicia_pub_not_printed = indicia_pub_not_printed
            entry.brand = brand
            entry.no_brand = no_brand
            entry.publication_date = publication_date
            entry.key_date = key_date
            entry.sort_code = sort_code
            entry.price = price
            entry.page_count = page_count
            entry.page_count_uncertain = page_count_uncertain
            entry.indicia_frequency = indicia_frequency
            entry.no_indicia_frequency = no_indicia_frequency
            entry.editing = editing
            entry.no_editing = no_editing
            entry.notes = notes
            entry.created = created
            entry.modified = modified
            entry.reserved = reserved
            entry.deleted = deleted
            entry.is_indexed = is_indexed
            entry.isbn = isbn
            entry.valid_isbn = valid_isbn
            entry.no_isbn = no_isbn
            entry.variant_of_id = variant_of_id
            entry.variant_name = variant_name
            entry.barcode = barcode
            entry.no_barcode = no_barcode
            entry.title = title
            entry.no_title = no_title
            entry.on_sale_date = on_sale_date
            entry.on_sale_date_uncertain = on_sale_date_uncertain
            entry.rating = rating
            entry.no_rating = no_rating
            entry.publisher_name = publisher_name
            entry.save()
        except Issue.DoesNotExist:
            print("ImportIssue: Inserting: " + str(id))
            Issue.objects.create(
                issue_id=id,
                number=number,
                volume = volume,
                no_volume = no_volume,
                display_volume_with_number = display_volume_with_number,
                series = series,
                indicia_publisher = indicia_publisher,
                indicia_pub_not_printed = indicia_pub_not_printed,
                brand = brand,
                no_brand = no_brand,
                publication_date = publication_date,
                key_date = key_date,
                sort_code = sort_code,
                price = price,
                page_count = page_count,
                page_count_uncertain = page_count_uncertain,
                indicia_frequency = indicia_frequency,
                no_indicia_frequency = no_indicia_frequency,
                editing = editing,
                no_editing = no_editing,
                notes = notes,
                created = created,
                modified = modified,
                reserved = reserved,
                deleted = deleted,
                is_indexed = is_indexed,
                isbn = isbn,
                valid_isbn = valid_isbn,
                no_isbn = no_isbn,
                variant_of_id = variant_of_id,
                variant_name = variant_name,
                barcode = barcode,
                no_barcode = no_barcode,
                title = title,
                no_title = no_title,
                on_sale_date = on_sale_date,
                on_sale_date_uncertain = on_sale_date_uncertain,
                rating = rating,
                no_rating = no_rating,
                publisher_name=publisher_name,
            )