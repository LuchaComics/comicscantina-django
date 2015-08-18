# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='city',
            new_name='billing_city',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='country',
            new_name='billing_country',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='phone',
            new_name='billing_phone',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='postal',
            new_name='billing_postal',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='province',
            new_name='billing_province',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='street_name',
            new_name='billing_street_name',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='street_number',
            new_name='billing_street_number',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='unit_number',
            new_name='billing_unit_number',
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_city',
            field=models.CharField(default='London', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_country',
            field=models.CharField(default='Canada', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_phone',
            field=models.CharField(blank=True, null=True, max_length=15),
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_postal',
            field=models.CharField(default='N6J4X4', max_length=31),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_province',
            field=models.CharField(default='Ontario', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_street_name',
            field=models.CharField(default='Centre Street', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_street_number',
            field=models.CharField(default='120', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_unit_number',
            field=models.CharField(blank=True, null=True, max_length=15),
        ),
    ]
