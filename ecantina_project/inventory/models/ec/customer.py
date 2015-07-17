import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models.ec.imageupload import ImageUpload


class Customer(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('last_name','first_name')
        db_table = 'ec_customers'
    
    # System
    customer_id = models.AutoField(primary_key=True)
    joined = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Name & Contact
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Address
    street_name = models.CharField(max_length=63)
    street_number = models.CharField(max_length=15)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63)
    province = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    postal = models.CharField(max_length=31)
    
    # Legal
    has_consented = models.BooleanField(default=False)
    
    # References.
    user = models.ForeignKey(User, null=True, blank=True)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (ID: ' + str(self.customer_id) + ')'