from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from django.core.cache import caches


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
    
    # Email Verification
    is_verified = models.BooleanField(default=False)
    verification_key = models.CharField(max_length=63, default='')
    
    joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    is_tos_signed = models.BooleanField(default=False)
    
    # References.
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization, db_index=True)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Employee, self).save(*args, **kwargs)