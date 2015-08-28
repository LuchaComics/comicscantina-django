# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150827_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='receipt',
        ),
        migrations.AddField(
            model_name='receipt',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='receipt_products', to='api.Product'),
        ),
    ]
