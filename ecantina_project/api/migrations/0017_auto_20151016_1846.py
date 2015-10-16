# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20151016_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='shipping_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='receipt',
            name='sub_total_with_tax',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
