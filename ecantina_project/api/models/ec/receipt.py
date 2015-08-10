from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.product import Product
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


class Receipt(models.Model):
    class Meta:
        app_label = 'inventory'
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
    
    # Financial
    products = models.ManyToManyField(Product)
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

    def __str__(self):
        return str(self.receipt_id)