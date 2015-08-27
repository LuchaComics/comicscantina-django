from django.db import models
from django.core.validators import MinValueValidator
from api.models.ec.organization import Organization


class Category(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_categories'
    
    category_id = models.AutoField(primary_key=True)
    parent_id = models.PositiveIntegerField(
        default=0,
    )
    name = models.CharField(max_length=127)
    def __str__(self):
        return str(self.name)