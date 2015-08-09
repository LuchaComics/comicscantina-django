from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.purchase import Purchase
from api.models.ec.customer import Customer


PURCHASE_TYPE_CHOICES = (
    (1, 'Store'),
    (2, 'Online'),
)

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


class Receipt(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('purchased_date',)
        db_table = 'ec_receipts'
    
    # Meta & Data-Mining
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store)
    customer = models.ForeignKey(Customer, null=True, blank=True,)
    receipt_id = models.AutoField(primary_key=True)
    purchased_date = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        default=1,
        choices=PURCHASE_TYPE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
    )
    payment_method = models.PositiveSmallIntegerField(
        default=1,
        choices=PAYMENT_METHOD_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    
    # Billing Information
    has_custom_billing_address = models.BooleanField(default=False)
    first_name = models.CharField(max_length=63, null=True, blank=True)
    last_name = models.CharField(max_length=63, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    street_name = models.CharField(max_length=63, null=True, blank=True)
    street_number = models.CharField(max_length=15, null=True, blank=True)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63, null=True, blank=True)
    province = models.CharField(max_length=63, null=True, blank=True)
    country = models.CharField(max_length=63, null=True, blank=True)
    postal = models.CharField(max_length=31, null=True, blank=True)

    # Financial
    purchases = models.ManyToManyField(Purchase)
    sub_total = models.DecimalField(
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

    def __str__(self):
        return str(self.receipt_id)