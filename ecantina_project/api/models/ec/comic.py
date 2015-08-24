from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from api.models.gcd.issue import Issue
from api.models.gcd.image import GCDImage
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.imageupload import ImageUpload
from api.models.ec.product import Product


CGC_RATING_OPTIONS = (
    (10.0, 'Gem Mint'),
    (9.9, 'Mint'),
    (9.8, 'Near Mint/Mintt'),
    (9.6, 'Near Mint +'),
    (9.4, 'Near Mint'),
    (9.2, 'Near Mint -'),
    (9.0, 'Very Fine/Near Mint'),
    (8.5, 'Very Fine +'),
    (8.0, 'Very Fine'),
    (7.5, 'Very Fine -'),
    (7.0, 'Fine/Very Fine'),
    (6.5, 'Fine +'),
    (6.0, 'Fine'),
    (5.5, 'Fine -'),
    (5.0, 'Very Good/Fine'),
    (4.5, 'Very Good +'),
    (4.0, 'Very Good'),
    (3.5, 'Very Good -'),
    (3.0, 'Good/Very Good'),
    (2.5, 'Good +'),
    (2.0, 'Good'),
    (1.8, 'Good -'),
    (1.5, 'Fair/Good'),
    (1.0, 'Fair'),
    (.5, 'Poor'),
)


LABEL_COLOUR_OPTIONS = (
    ('Purple', 'Purple'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Yellow', 'Yellow'),
)


CONDITION_RATING_RATING_OPTIONS = (
    (10, 'Near Mint'),
    (8, 'Very Fine'),
    (6, 'Fine'),
    (4, 'Very Good'),
    (2, 'Good'),
    (1, 'Fair'),
    (0, 'Poor'),
)


AGE_OPTIONS = (
    (1, 'Gold'),
    (2, 'Silver'),
    (3, 'Bronze'),
    (4, 'Copper'),
)


class Comic(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('issue',)
        db_table = 'ec_comics'
    
    comic_id = models.AutoField(primary_key=True)
    is_cgc_rated = models.BooleanField(default=False)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=AGE_OPTIONS,
        null=True,
        blank=True,
    )
    cgc_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        choices=CGC_RATING_OPTIONS,
        null=True,
        blank=True,
    )
    label_colour = models.CharField(
        max_length=63,
        choices=LABEL_COLOUR_OPTIONS,
        null=True,
        blank=True,
    )
    condition_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        choices=CONDITION_RATING_RATING_OPTIONS,
        null=True,
        blank=True,
    )
    is_canadian_priced_variant = models.BooleanField(default=False)
    is_variant_cover = models.BooleanField(default=False)
    is_retail_incentive_variant = models.BooleanField(default=False)
    is_newsstand_edition = models.BooleanField(default=False)
    
    product = models.ForeignKey(Product)
    issue = models.ForeignKey(Issue)
   
    def __str__(self):
        return str(self.issue)

    def delete(self, *args, **kwargs):
        """
            Deleting comic entry automatically deletes the foreign key.
        """
        if self.product:
            self.product.delete()
        super(Comic, self).delete(*args, **kwargs) # Call the "real" delete() method