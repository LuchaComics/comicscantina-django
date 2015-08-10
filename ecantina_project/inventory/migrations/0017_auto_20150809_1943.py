# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20150809_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='purchases',
        ),
        migrations.AddField(
            model_name='receipt',
            name='discount_amount',
            field=models.DecimalField(default=0.0, decimal_places=2, max_digits=10),
        ),
        migrations.AddField(
            model_name='receipt',
            name='products',
            field=models.ManyToManyField(to='inventory.Product'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'Store'), (2, 'Online'), (3, 'Convention')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
