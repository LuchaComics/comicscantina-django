# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchased_date', models.DateTimeField(auto_now_add=True)),
                ('sub_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tax_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('customer', models.ForeignKey(to='inventory.Customer')),
                ('product', models.ForeignKey(to='inventory.Product')),
            ],
            options={
                'db_table': 'ec_purchases',
                'ordering': ('purchased_date',),
            },
        ),
    ]
