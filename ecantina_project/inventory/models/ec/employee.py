import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store

ROLE_CHOICES = (
    (settings.EMPLOYEE_OWNER_ROLE, 'Owner'),
    (settings.EMPLOYEE_MANAGER_ROLE, 'Manager'),
    (settings.EMPLOYEE_CLERC_ROLE, 'Clerc'),
    (settings.EMPLOYEE_CASHIER_ROLE, 'Cashier'),
)

class Employee(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('employee_id',)
        db_table = 'ec_employees'
    
    # System
    employee_id = models.AutoField(primary_key=True)
    role = models.PositiveSmallIntegerField(
        default=0,
        choices=ROLE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    joined = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Address
    street_name = models.CharField(max_length=63)
    street_number = models.CharField(max_length=15)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63)
    province = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    postal = models.CharField(max_length=31)
    
    # Contact
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # References.
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name