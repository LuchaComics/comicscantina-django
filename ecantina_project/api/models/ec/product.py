from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.comic import Comic


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
    
    # Product Supported References
    comic = models.ForeignKey(Comic, null=True, blank=True)
    # Add more future products here ...
    
    def __str__(self):
        return str(self.product_id) + " " + str(self.type)
