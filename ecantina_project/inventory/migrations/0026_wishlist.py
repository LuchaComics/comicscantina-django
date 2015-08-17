# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_promotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(to='inventory.Customer')),
                ('products', models.ManyToManyField(to='inventory.Product')),
            ],
            options={
                'db_table': 'ec_wishlists',
            },
        ),
    ]
