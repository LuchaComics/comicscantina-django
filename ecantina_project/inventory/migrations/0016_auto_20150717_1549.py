# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20150714_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, to='inventory.Customer', null=True)),
                ('employee', models.ForeignKey(blank=True, to='inventory.Employee', null=True)),
            ],
            options={
                'db_table': 'ec_carts',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Comic'), (2, 'Furniture'), (3, 'Coin'), (4, 'General')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comics', models.ForeignKey(blank=True, to='inventory.Comic', null=True)),
            ],
            options={
                'db_table': 'ec_products',
                'ordering': ('product_id', 'type'),
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='inventory.Product'),
        ),
    ]
