from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches


class SubDomain(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_subdomains'
    
    sub_domain_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True, unique=True,)
    organization = models.ForeignKey(Organization, null=True, blank=True, db_index=True)
    store = models.ForeignKey(Store, null=True, blank=True, db_index=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(SubDomain, self).save(*args, **kwargs)
