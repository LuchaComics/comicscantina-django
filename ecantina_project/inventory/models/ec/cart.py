from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.customer import Customer
from inventory.models.ec.product import Product


class Cart(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('created',)
        db_table = 'ec_carts'
    
    customer = models.ForeignKey(Customer, null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, blank=True)
    product = models.ManyToManyField(Product)
    cart_id = models.AutoField(primary_key=True)
    created = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.cart_id) + " " + str(self.created)