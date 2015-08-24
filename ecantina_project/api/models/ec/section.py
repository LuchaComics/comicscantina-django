from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from api.models.ec.organization import Organization
from api.models.ec.store import Store


class Section(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_sections'
    
    section_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True)
    store = models.ForeignKey(Store)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name