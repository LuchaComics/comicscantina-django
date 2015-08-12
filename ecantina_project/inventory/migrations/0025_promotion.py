# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20150811_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('promotion_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10, default=0.0)),
                ('discount_type', models.PositiveSmallIntegerField(choices=[(1, '%'), (2, '$')], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('organization', models.ForeignKey(to='inventory.Organization')),
            ],
            options={
                'db_table': 'ec_promotions',
                'ordering': ('name',),
            },
        ),
    ]
