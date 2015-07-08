import os
from django.db import models
from django.contrib.auth.models import User
from inventory.models.ec.organization import Organization
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.employee import Employee


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
    
    # Hours
    is_open_monday = models.BooleanField(default=False)
    is_open_tuesday = models.BooleanField(default=False)
    is_open_wednesday = models.BooleanField(default=False)
    is_open_thursday = models.BooleanField(default=False)
    is_open_friday = models.BooleanField(default=False)
    is_open_saturday = models.BooleanField(default=False)
    is_open_sunday = models.BooleanField(default=False)
    
    monday_to = models.CharField(max_length=7, null=True, blank=True)
    tuesday_to = models.CharField(max_length=7, null=True, blank=True)
    wednesday_to = models.CharField(max_length=7, null=True, blank=True)
    thursday_to = models.CharField(max_length=7, null=True, blank=True)
    friday_to = models.CharField(max_length=7, null=True, blank=True)
    saturday_to = models.CharField(max_length=7, null=True, blank=True)
    sunday_to = models.CharField(max_length=7, null=True, blank=True)
    
    monday_from = models.CharField(max_length=7, null=True, blank=True)
    tuesday_from = models.CharField(max_length=7, null=True, blank=True)
    wednesday_from = models.CharField(max_length=7, null=True, blank=True)
    thursday_from = models.CharField(max_length=7, null=True, blank=True)
    friday_from = models.CharField(max_length=7, null=True, blank=True)
    saturday_from = models.CharField(max_length=7, null=True, blank=True)
    sunday_from = models.CharField(max_length=7, null=True, blank=True)
    
    # Reference
    organization = models.ForeignKey(Organization)
    employees = models.ManyToManyField(Employee)
    logo = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name