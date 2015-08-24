from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization


class Brand(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_brands'
    
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    organization = models.ForeignKey(Organization)
    def __str__(self):
        return str(self.name)