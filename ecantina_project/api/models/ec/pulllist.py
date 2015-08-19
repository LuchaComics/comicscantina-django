from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.gcd.publisher import Publisher
from api.models.gcd.series import Series

class Pulllist(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('series',)
        db_table = 'ec_pulllists'
    
    pulllist_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization)
    series = models.ForeignKey(Series, null=True)
    publisher = models.ForeignKey(Publisher)
    customers = models.ManyToManyField(Customer)
    
    def __str__(self):
        return self.name