from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from django.core.cache import caches


class Customer(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('last_name','first_name')
        db_table = 'ec_customers'
    
    # System
    customer_id = models.AutoField(primary_key=True)
    joined = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    
    # Name & Contact
    first_name = models.CharField(max_length=63, db_index=True)
    last_name = models.CharField(max_length=63, db_index=True)
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    
    # Billing Info
    billing_name = models.CharField(max_length=126)
    billing_phone = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    billing_street_name = models.CharField(max_length=63)
    billing_street_number = models.CharField(max_length=15)
    billing_unit_number = models.CharField(max_length=15, null=True, blank=True)
    billing_city = models.CharField(max_length=63)
    billing_province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    billing_country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    billing_postal = models.CharField(max_length=31, db_index=True)
    
    # Shipping Info
    shipping_name = models.CharField(max_length=126)
    shipping_phone = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    shipping_street_name = models.CharField(max_length=63)
    shipping_street_number = models.CharField(max_length=15)
    shipping_unit_number = models.CharField(max_length=15, null=True, blank=True)
    shipping_city = models.CharField(max_length=63)
    shipping_province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    shipping_country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    shipping_postal = models.CharField(max_length=31, db_index=True)
    
    # Legal
    has_consented = models.BooleanField(default=False)
    
    # References.
    user = models.ForeignKey(User, null=True, blank=True)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True)
    qrcode = models.ImageField(upload_to='qrcode', null=True, blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (ID: ' + str(self.customer_id) + ')'

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Customer, self).save(*args, **kwargs)
