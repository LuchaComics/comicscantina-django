from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.product import Product


class Receipt(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('last_updated',)
        db_table = 'ec_receipts'
    
    # Meta & Data-Mining
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store)
    employee = models.ForeignKey(Employee, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True,)
    receipt_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    has_purchased_online = models.BooleanField(default=False)
    payment_method = models.PositiveSmallIntegerField(
        default=1,
        choices=constants.PAYMENT_METHOD_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    status = models.PositiveSmallIntegerField(
        default=1,
        choices=constants.STATUS_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    
    # Financial
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    has_tax = models.BooleanField(default=True)
    tax_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    has_finished = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)
    
    # Payer Information
    email = models.EmailField(null=True, blank=True)
    billing_first_name = models.CharField(max_length=63, null=True, blank=True)
    billing_last_name = models.CharField(max_length=63, null=True, blank=True)
    billing_address = models.CharField(max_length=63, null=True, blank=True)
    billing_phone = models.CharField(max_length=10, null=True, blank=True)
    billing_city = models.CharField(max_length=63, null=True, blank=True)
    billing_province = models.CharField(max_length=63, null=True, blank=True)
    billing_country = models.CharField(max_length=63, null=True, blank=True)
    billing_postal = models.CharField(max_length=31, null=True, blank=True)
    shipping_first_name = models.CharField(max_length=63, null=True, blank=True)
    shipping_last_name = models.CharField(max_length=63, null=True, blank=True)
    shipping_address = models.CharField(max_length=63, null=True, blank=True)
    shipping_phone = models.CharField(max_length=10, null=True, blank=True)
    shipping_city = models.CharField(max_length=63, null=True, blank=True)
    shipping_province = models.CharField(max_length=63, null=True, blank=True)
    shipping_country = models.CharField(max_length=63, null=True, blank=True)
    shipping_postal = models.CharField(max_length=31, null=True, blank=True)

    # This variable is used to track all the "Products" that are either
    # checked out or are to be purchased (in cart).
    products = models.ManyToManyField(Product, blank=True, related_name='receipt_products')

    def __str__(self):
        return "Receipt #" + str(self.receipt_id) + " - " + self.billing_first_name + " " + self.billing_last_name