# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20151019_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='has_shipping',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
