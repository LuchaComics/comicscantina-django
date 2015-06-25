import os
from django.db import models
from django.contrib.auth.models import User
from inventory.models.ec.organization import Organization
from inventory.models.ec.imageupload import ImageUpload


class Store(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('store_id',)
        db_table = 'ec_stores'
    
    # Basic
    store_id = models.AutoField(primary_key=True)
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
    
    # Reference
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name