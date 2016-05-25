import os
import sys
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


LARGE_ZOOM = 4
MEDIUM_ZOOM = 2
SMALL_ZOOM = 1
NO_ZOOM = 0
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2

PNG_EXTENSION = 'png'
JPG_EXTENSION = 'jpg'
JPEG_EXTENSION = 'jpeg'
TIFF_EXTENSION = 'tiff'
JFIF_EXTENSION = 'jfif'
GIF_EXTENSION = 'gif'
BMP_EXTENSION = 'bmp'
UNKNOWN_EXTENSION = 'unknown'

SUPPORTED_FILE_EXTENSIONS = ['.png', '.jpeg',  '.jpg',  '.bmp',  '.tiff', '.gif']

ZOOM_LEVEL_CHOICES = (
    (NO_ZOOM, 'No Zoom'),
    (SMALL_ZOOM, 'Small Zoom'),
    (MEDIUM_ZOOM, 'Medium Zoom'),
    (LARGE_ZOOM, 'Large zoom'),
)

CATEGORY_CHOICES = (
    (PRIMARY_IMAGE, 'Primary'),
    (ALTERNATIVE_IMAGE, 'Alternate'),
)

IMAGE_FORMAT_EXTENSION_CHOICES = (
    (PNG_EXTENSION, 'Portable Network Graphics (PNG)'),
    (JPEG_EXTENSION, 'Joint Photographic Experts Group picture (JPEG'),
    (JPG_EXTENSION, 'Joint Photographic Experts Group picture (JPG'),
    (BMP_EXTENSION, 'Bitmap Image File (BMP'),
    (TIFF_EXTENSION, 'Tagged Image File Format (TIFF'),
    (GIF_EXTENSION, 'Graphics Interchange Format (GIF'),
)

# Note: http://www.freeformatter.com/mime-types-list.html
PNG_MIMETYPE = 'image/png'
JPEG_MIMETYPE = 'image/jpeg'
BMP_MIMETYPE = 'image/bmp'
TIFF_MIMETYPE = 'image/tiff'
GIF_MIMETYPE = 'image/gif'
MIMETYPE_CHOICES = (
    (PNG_MIMETYPE, 'PNG'),
    (JPEG_MIMETYPE, 'JPEG/JPG'),
    (BMP_MIMETYPE, 'BMP'),
    (TIFF_MIMETYPE, 'TIFF'),
    (GIF_MIMETYPE, 'GIF'),
)


class CCImageBinary(models.Model):
    class Meta:
        app_label = 'catalog'
        db_table = 'gcd_image_binaries'

    id = models.AutoField(primary_key=True, db_index=True)
    data = models.BinaryField()

    def __str__(self):
        return "Image #" + str(self.id)


class CCImage(models.Model):
    class Meta:
        app_label = 'catalog'
        db_table = 'gcd_images'

    id = models.AutoField(primary_key=True, db_index=True)
    filename = models.CharField(db_index=True, max_length=127, null=True, blank=True, unique=True,)
    category = models.PositiveSmallIntegerField(
        db_index=True,
        default=PRIMARY_IMAGE,
        choices=CATEGORY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
    )
    zoom_level = models.PositiveSmallIntegerField(
        db_index=True,
        default=NO_ZOOM,
        choices=ZOOM_LEVEL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
    )
    file_type = models.CharField(
        db_index=True,
        max_length=4,
        choices=IMAGE_FORMAT_EXTENSION_CHOICES,
    )
    mime_type = models.CharField(
        db_index=True,
        default=JPEG_MIMETYPE,
        max_length=15,
        choices=MIMETYPE_CHOICES,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    binary = models.ForeignKey(CCImageBinary)

    def __str__(self):
        return "Image #" + str(self.id)

class CCSeries(models.Model):
    class Meta:
        app_label = 'catalog'
        db_table = 'gcd_series'

    series_id = models.PositiveIntegerField(primary_key=True, db_index=True,)
    image = models.ForeignKey(CCImage, null=True, blank=True, related_name="primary_image", )
    alt_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="alternative_image", )
    has_images = models.BooleanField(default=False,db_index=True)
    is_missing_cover = models.BooleanField(default=False,db_index=True)
    publisher_id = models.PositiveIntegerField(db_index=True,)
    country_id = models.PositiveIntegerField(db_index=True,)
    language_id = models.PositiveIntegerField(db_index=True,)

    def __str__(self):
        return "Series #" + str(self.series_id)

class CCIssue(models.Model):
    class Meta:
        app_label = 'catalog'
        db_table = 'gcd_issues'

    issue_id = models.PositiveIntegerField(primary_key=True, db_index=True,)
    small_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="primary_small_image", )
    medium_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="primary_medium_image", )
    large_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="primary_large_image", )
    alt_small_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="alternative_small_image", )
    alt_medium_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="alternative_medium_image", )
    alt_large_image = models.ForeignKey(CCImage, null=True, blank=True, related_name="alternative_large_image", )
    has_images = models.BooleanField(default=False,db_index=True)
    is_missing_cover = models.BooleanField(default=False,db_index=True)
    publisher_id = models.PositiveIntegerField(db_index=True,)
    country_id = models.PositiveIntegerField(db_index=True,)
    language_id = models.PositiveIntegerField(db_index=True,)
    series = models.ForeignKey(CCSeries)

    def __str__(self):
        return "Issue #" + str(self.issue_id)


# Import the libraries used for saving a binary to file.
import base64
import io
from django.core.files import File


# Import the models we will be using for importing.
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue


import requests
from django.core.files import File


IMAGE_SERVER_BASEL_URL = "http://127.0.0.1:8000/image/"


class Command(BaseCommand):
    help = 'ETL iterates all the entries in the db.sqlite3 database and uploads the images to Amazon S3.'

    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        # self.save_all_series()
        self.save_all_issues()

    def download_file(self, url):
        """
        Downloads the file to the filesystem.
        """
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
        # Source:
        #    https://vinta.ws/code/read-and-save-file-in-django-python.html
        #

    def delete_at_filepath(self, filepath):
        """
        Delete the file at this location.
        """
        if os.path.isfile(filepath):
            os.remove(filepath)

    def save_all_series(self):
        """
        Save all series.
        """
        series = GCDSeries.objects.all().order_by("series_id")
        for a_series in series.all():
            # Generate the file name.
            filename = str(a_series.series_id) + ".jpg"

            # Generate the URL to access.
            url = IMAGE_SERVER_BASEL_URL + filename

            # Download the file locally from the URL.
            filepath = self.download_file(url);

            # Get the Image & save it to our model which will upload to
            # our Amazon S3 service.
            with open(filepath, 'rb') as f:
                f = File(f)
                a_series.cover = f
                a_series.save()

            # Delete the local file.
            self.delete_at_filepath(filepath)

            print("Series ID:", a_series.series_id, "- Saved")
            sleep(1)

    def save_all_issues(self):
        """
        Save all issues.
        """
        # issues = GCDIssue.objects.all()
        issues = GCDIssue.objects.filter(issue_id=111)
        for an_issue in issues.all():
            try:
                filename = str(an_issue.issue_id)

                # Small Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_1.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.small_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                # Medium Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_2.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.medium_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                # Large Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_4.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.large_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                # Alt Small Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_1.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.alt_small_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                # Alt Medium Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_2.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.alt_medium_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                # Alt Large Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_4.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    an_issue.alt_large_image = File(f)
                    an_issue.save()
                self.delete_at_filepath(filepath)

                print("Issue ID:", an_issue.issue_id, "- Saved")
            except GCDIssue.DoesNotExist:
                print("Issue ID:", an_issue.issue_id, "- Skipped")
            sleep(1) # Add artifical delay.
