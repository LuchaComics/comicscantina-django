import os
from django.db import models
from django.contrib.auth.models import User
from inventory.models.ec.organization import Organization


class Store(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('store_id',)
        db_table = 'ec_stores'
    
    # Basic
    store_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='upload', null=True, blank=True)
    name = models.CharField(max_length=127)
    description = models.TextField(null=True, blank=True)
    joined = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Location
    street_name = models.CharField(max_length=63)
    street_number = models.CharField(max_length=31, null=True, blank=True)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63)
    province = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    postal = models.CharField(max_length=31)
    
    # Contact
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=31, null=True, blank=True)
    fax = models.CharField(max_length=31, null=True, blank=True)
    
    # Social Media
    twitter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    google_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    flickr_url = models.URLField(null=True, blank=True)

    # Reference
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
                super(Store, self).delete(*args, **kwargs) # Call the "real" delete() method