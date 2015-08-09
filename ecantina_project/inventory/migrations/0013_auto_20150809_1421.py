# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_cart_has_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_price',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0.0),
        ),
    ]
