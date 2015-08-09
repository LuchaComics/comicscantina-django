# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_product_discount_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='has_tax',
            field=models.BooleanField(default=True),
        ),
    ]
