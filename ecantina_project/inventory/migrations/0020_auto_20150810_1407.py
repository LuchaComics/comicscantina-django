# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_cart_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0.0),
        ),
        migrations.AddField(
            model_name='store',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0.13),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'In-Store Purchase'), (2, 'Online Purchase'), (3, 'Convention Purchase')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
