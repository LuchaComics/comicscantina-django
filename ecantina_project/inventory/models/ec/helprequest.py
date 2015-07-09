from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee

SUBJECT_CHOICES = (
    (1, 'Feedback'),
    (2, 'Error'),
    (3, 'Checkout'),
    (4, 'Inventory'),
    (5, 'Pull List'),
    (6, 'Sales'),
    (7, 'Emailing List'),
    (8, 'Store Settings / Users'),
    (9, 'Dashboard'),
)

class HelpRequest(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('submission_date',)
        db_table = 'ec_help_requests'
    
    help_id = models.AutoField(primary_key=True)
    subject = models.PositiveSmallIntegerField(
        default=1,
        choices=SUBJECT_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    subject_url = models.URLField(null=True, blank=True)
    message = models.TextField(null=True)
    submission_date = models.DateField(auto_now=True, null=True)
    
    # References
    screenshot = models.ForeignKey(ImageUpload, null=True, blank=True)
    employee = models.ForeignKey(Employee)
    store = models.ForeignKey(Store)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name