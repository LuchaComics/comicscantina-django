# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='country',
            field=models.ForeignKey(null=True, to='inventory.Country'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='type',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)], default=1, choices=[(1, 'Store'), (2, 'Online')]),
        ),
    ]
