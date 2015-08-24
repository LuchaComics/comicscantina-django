from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization


DISCOUNT_TYPE_OPTIONS = (
    (1, '%'),
    (2, '$'),
)


class Tag(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_tags'
    
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    discount = models.DecimalField( # Note: Meaured in dollar ($) amount.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=DISCOUNT_TYPE_OPTIONS,
        default=1,
    )
    organization = models.ForeignKey(Organization)
    def __str__(self):
        return str(self.tag_id)