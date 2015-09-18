import os
from django.db import models
from django.contrib.auth.models import User
from api.models.ec.organization import Organization
from api.models.ec.imageupload import ImageUpload
from api.models.ec.employee import Employee

STORE_HOUR_OPTIONS = (
    ('08:00', '08:00'),
    ('08:30', '08:30'),
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
    ('18:00', '18:00'),
    ('18:30', '18:30'),
    ('19:00', '19:00'),
    ('19:30', '19:30'),
    ('20:00', '20:00'),
    ('20:30', '20:30'),
    ('21:00', '21:00'),
    ('21:30', '21:30'),
    ('22:00', '22:00'),
    ('22:30', '22:30'),
)

class Store(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('store_id',)
        db_table = 'ec_stores'
    
    # Basic
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    description = models.TextField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    tax_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.13, # Ontario HST
    )
    
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
    
    monday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_to = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    
    monday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_from = models.CharField(choices=STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    
    # Reference
    organization = models.ForeignKey(Organization)
    employees = models.ManyToManyField(Employee)
    logo = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name