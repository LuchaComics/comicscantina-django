from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization


class Employee(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('employee_id',)
        db_table = 'ec_employees'
    
    # System
    employee_id = models.AutoField(primary_key=True)
    role = models.PositiveSmallIntegerField(
        default=0,
        choices=constants.ROLE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    
    # Address
    street_name = models.CharField(max_length=63)
    street_number = models.CharField(max_length=15)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63)
    province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    postal = models.CharField(max_length=31)
    
    # Contact
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # References.
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)