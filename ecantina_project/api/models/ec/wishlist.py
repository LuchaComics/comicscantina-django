from django.db import models
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from django.core.cache import caches


class Wishlist(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'ec_wishlists'
    
    wishlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Wishlist, self).save(*args, **kwargs)