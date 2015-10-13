# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151009_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_aggregated',
            field=models.BooleanField(default=True),
        ),
    ]
