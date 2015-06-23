from django.db import models
from inventory.models.gcd.country import Country
from inventory.models.gcd.image import Image


class Publisher(models.Model):
    class Meta:
        app_label = 'inventory'
        ordering = ('name',)
        db_table = 'gcd_publishers'
    
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    year_began = models.PositiveSmallIntegerField(db_index=True, null=True)
    year_ended = models.PositiveSmallIntegerField(null=True)
    year_began_uncertain = models.BooleanField(default=False, blank=True, db_index=True)
    year_ended_uncertain = models.BooleanField(default=False, blank=True, db_index=True)
    notes = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, max_length=255, blank=True, default=u'')
    is_master = models.BooleanField(default=False, blank=True, db_index=True)
    
    # Fields related to change management.
    reserved = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, db_index=True)

    # Cached counts.
    imprint_count = models.IntegerField(default=0)
    brand_count = models.IntegerField(default=0, db_index=True)
    indicia_publisher_count = models.IntegerField(default=0, db_index=True)
    series_count = models.IntegerField(default=0)
    issue_count = models.IntegerField(default=0)

    # Referenced
    country = models.ForeignKey(Country)
    images = models.ManyToManyField(Image)
    parent = models.ForeignKey('self', null=True,
                                related_name='imprint_set')

    def __str__(self):
        return self.name