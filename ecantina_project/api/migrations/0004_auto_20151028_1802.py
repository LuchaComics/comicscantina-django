# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151028_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnifiedShippingRate',
            fields=[
                ('shipping_rate_id', models.AutoField(serialize=False, primary_key=True)),
                ('country', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(124, 'Canada'), (840, 'United States'), (484, 'Mexico')], validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(840)])),
                ('comics_rate1', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate2', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate3', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate4', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate5', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate6', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate7', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate8', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate9', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
                ('comics_rate10', models.DecimalField(default=0.0, max_digits=10, decimal_places=2, db_index=True)),
            ],
            options={
                'ordering': ('country',),
                'db_table': 'ec_unified_shipping_rates',
            },
        ),
        migrations.AddField(
            model_name='store',
            name='has_shipping_rate_override',
            field=models.BooleanField(default=False),
        ),
    ]
