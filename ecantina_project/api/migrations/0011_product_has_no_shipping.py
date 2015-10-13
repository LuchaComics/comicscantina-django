# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_store_is_aggregated'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_no_shipping',
            field=models.BooleanField(default=False),
        ),
    ]
