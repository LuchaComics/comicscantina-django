from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from api.models.gcd.country import Country
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.product import Product


PURCHASE_TYPE_CHOICES = (
    (1, 'Store'),
    (2, 'Online'),
)


class Purchase(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('purchased_date',)
        db_table = 'ec_purchases'
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    purchase_id = models.AutoField(primary_key=True)
    purchased_date = models.DateTimeField(auto_now_add=True)
    sub_amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )
    tax_amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )
    type = models.PositiveSmallIntegerField(
        default=1,
        choices=PURCHASE_TYPE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    country = models.ForeignKey(Country, null=True, default=250)

    def __str__(self):
        return str(self.purchase_id)