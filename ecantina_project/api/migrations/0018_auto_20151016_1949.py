# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151016_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_tax',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_price_with_tax',
            field=models.DecimalField(max_digits=10, default=0.0, decimal_places=2),
        ),
        migrations.AddField(
            model_name='product',
            name='tax_amount',
            field=models.DecimalField(max_digits=10, default=0.0, decimal_places=2),
        ),
        migrations.AddField(
            model_name='product',
            name='tax_rate',
            field=models.DecimalField(max_digits=10, default=0.0, decimal_places=2),
        ),
    ]
