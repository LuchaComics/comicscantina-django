from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.imageupload import ImageUpload
from api.models.ec.receipt import Receipt


PRODUCT_TYPE_OPTIONS = (
    (settings.COMIC_PRODUCT_TYPE, 'Comic'),
    (settings.FURNITURE_PRODUCT_TYPE, 'Furniture'),
    (settings.COIN_PRODUCT_TYPE, 'Coin'),
    #(settings.GENERAL_PRODUCT_TYPE, 'General'),
)

PRODUCT_DISCOUNT_TYPE_OPTIONS = (
    (1, '%'),
    (2, '$'),
)

class Product(models.Model):
    """
        Model acts as an encompasing object to hold all the different
        type of products in our system such as comics, furniture, etc.
    """
    class Meta:
        app_label = 'api'
        ordering = ('product_id','type')
        db_table = 'ec_products'
    
    # All products have a unque 'product_id' number which is to be
    # printed on all products in-store or online.
    product_id = models.AutoField(primary_key=True)
    
    # Every product needs to have a generic name that will show up
    # when customers lookup the product and staff look through the
    # inventory database; furthermore, a product type needs to be
    # specified to tell what sort of product this is.
    name = models.CharField(max_length=127, null=True, blank=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=PRODUCT_TYPE_OPTIONS,
        default=1,
    )
    
    # Date & timekeeping tracking variables.
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # If this product has been purchased by a customer then "True" is set,
    # else "False". Stores are not to display products with 'True' condition.
    # It is important to note that when a product is purchased, the product
    # is not to be deleted from the table, but instead remain in the table
    # and just have the "is_sold" varible to be "True".
    is_sold = models.BooleanField(default=False)
    
    # The following variables are to save financial information.
    sub_price = models.DecimalField( # Note: Price before discount applied.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount = models.DecimalField( # Note: Meaured in dollar ($) amount.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=PRODUCT_DISCOUNT_TYPE_OPTIONS,
        default=1,
    )
    price = models.DecimalField( # Note: Price after discount applied.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
                              
    # Every product has images.
    image = models.ForeignKey(ImageUpload, null=True, blank=True, on_delete=models.SET_NULL)
    images = models.ManyToManyField(ImageUpload, blank=True, related_name='product_images')
    
    # Products need to belong to a specific organization and where it is located
    # in the organization (store/section).
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store)
    section = models.ForeignKey(Section)
    
    # Products need to be belong to a receipt once purchased.
    receipt = models.ForeignKey(Receipt, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
