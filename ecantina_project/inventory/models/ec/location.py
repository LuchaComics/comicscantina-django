from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from inventory.models.gcd.issue import Issue
from inventory.models.gcd.image import Image
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store


class Location(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('name',)
        db_table = 'ec_locations'
    
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True)
    store = models.ForeignKey(Store)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name