from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee


PAYMENT_METHOD_CHOICES = (
    (1, 'Cash'),
    (2, 'Debit Card'),
    (3, 'Credit Card'),
    (4, 'Gift Card'),
    (5, 'Store Points'),
    (6, 'Cheque'),
    (7, 'PayPal'),
    (8, 'Invoice'),
    (9, 'Other'),
)


STATUS_CHOICES = (
    (1, 'New Order'),
    (2, 'Picked'),
    (3, 'Shipped'),
    (4, 'Received'),
    (5, 'In-Store Sale'),
    (6, 'Online Sale'),
)


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
        choices=PAYMENT_METHOD_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    status = models.PositiveSmallIntegerField(
        default=1,
        choices=STATUS_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    
    # Financial
    products_count = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0),],
    )
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
    billing_first_name = models.CharField(max_length=63, null=True, blank=True)
    billing_last_name = models.CharField(max_length=63, null=True, blank=True)
    billing_address = models.CharField(max_length=63, null=True, blank=True)
    billing_email = models.EmailField(null=True, blank=True)
    billing_phone = models.CharField(max_length=15, null=True, blank=True)
    billing_city = models.CharField(max_length=63, null=True, blank=True)
    billing_province = models.CharField(max_length=63, null=True, blank=True)
    billing_country = models.CharField(max_length=63, null=True, blank=True)
    billing_postal = models.CharField(max_length=31, null=True, blank=True)
    shipping_first_name = models.CharField(max_length=63, null=True, blank=True)
    shipping_last_name = models.CharField(max_length=63, null=True, blank=True)
    shipping_address = models.CharField(max_length=63, null=True, blank=True)
    shipping_email = models.EmailField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_city = models.CharField(max_length=63, null=True, blank=True)
    shipping_province = models.CharField(max_length=63, null=True, blank=True)
    shipping_country = models.CharField(max_length=63, null=True, blank=True)
    shipping_postal = models.CharField(max_length=31, null=True, blank=True)

    def __str__(self):
        return str(self.receipt_id)