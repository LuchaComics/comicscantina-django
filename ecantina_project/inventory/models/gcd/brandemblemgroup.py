from django.db import models
from inventory.models.gcd.image import Image
from inventory.models.gcd.brand import Brand
from inventory.models.gcd.brandgroup import BrandGroup


class BrandEmblemGroup(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('brand',)
        db_table = 'gcd_brand_emblem_groups'
    
    brand_emblem_group_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, null=True)
    brandgroup = models.ForeignKey(BrandGroup, null=True)

    def __str__(self):
        return str(self.brand_emblem_group_id)
