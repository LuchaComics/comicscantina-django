from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.pulllist import Pulllist

class PulllistSubscription(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'ec_pulllists_subscriptions'
    
    subscription_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization)
    pulllist = models.ForeignKey(Pulllist)
    customer = models.ForeignKey(Customer)
    copies = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.subscription_id)