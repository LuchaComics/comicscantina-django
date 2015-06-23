import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    
    employee_id = models.AutoField(primary_key=True)
    role = models.PositiveSmallIntegerField(
        default=0,
        choices=ROLE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    image = models.ImageField(upload_to='upload', null=True, blank=True)
    store = models.ForeignKey(Store)
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
                super(Employee, self).delete(*args, **kwargs) # Call the "real" delete() method