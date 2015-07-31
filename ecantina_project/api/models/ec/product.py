from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.gcd.image import Image
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.imageupload import ImageUpload


PRODUCT_TYPE_OPTIONS = (
    (settings.COMIC_PRODUCT_TYPE, 'Comic'),
    (settings.FURNITURE_PRODUCT_TYPE, 'Furniture'),
    (settings.COIN_PRODUCT_TYPE, 'Coin'),
    (settings.GENERAL_PRODUCT_TYPE, 'General'),
)


class Product(models.Model):
    """
        Model acts as an encompasing object to hold all the different
        type of products in our system such as comics, furniture, etc.
    """
    class Meta:
        app_label = 'inventory'
        ordering = ('product_id','type')
        db_table = 'ec_products'
    
    # Basic
    product_id = models.AutoField(primary_key=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=PRODUCT_TYPE_OPTIONS,
        default=1,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    price = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    cost = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
                              
    # References
    image = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)
    images = models.ManyToManyField(ImageUpload, blank=True, related_name='product_images')
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store)
    section = models.ForeignKey(Section)
    
    def __str__(self):
        return str(self.product_id) + " " + str(self.type)
