from django.db import models
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.imageupload import ImageUpload
from api.models.ec.employee import Employee
from django.core.cache import caches


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
    is_suspended = models.BooleanField(default=False)
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
    province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    postal = models.CharField(max_length=31)
    currency = models.PositiveSmallIntegerField(
        default=124,
        choices=constants.ISO_4217_CURRENCY_OPTIONS,
    )
    language = models.CharField(
        max_length=2,
        choices=constants.ISO_639_1_LANGUAGE_OPTIONS,
        default='EN',
    )
    
    # Contact
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=10, null=True, blank=True)
    
    # Hours
    is_open_monday = models.BooleanField(default=False)
    is_open_tuesday = models.BooleanField(default=False)
    is_open_wednesday = models.BooleanField(default=False)
    is_open_thursday = models.BooleanField(default=False)
    is_open_friday = models.BooleanField(default=False)
    is_open_saturday = models.BooleanField(default=False)
    is_open_sunday = models.BooleanField(default=False)
    
    monday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    
    monday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    
    # The following columns determine if the particular store supports selling
    # the following products and thus granting access to unique user interface.
    is_comics_vendor = models.BooleanField(default=True)
    is_furniture_vendor = models.BooleanField(default=False)
    is_coins_vendor = models.BooleanField(default=False)
    
    # Reference
    organization = models.ForeignKey(Organization, db_index=True)
    employees = models.ManyToManyField(Employee)
    logo = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Store, self).save(*args, **kwargs)