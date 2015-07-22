from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.purchase import Purchase


class Receipt(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('purchased_date',)
        db_table = 'ec_receipts'
    
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store)
    purchases = models.ManyToManyField(Purchase)
    receipt_id = models.AutoField(primary_key=True)
    purchased_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )
    tax_amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )
    after_tax_amount = models.FloatField(
        validators=[MinValueValidator(0),],
        default=0,
    )

    def __str__(self):
        return str(self.receipt_id)