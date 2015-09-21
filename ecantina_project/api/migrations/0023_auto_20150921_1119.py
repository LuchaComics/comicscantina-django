# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20150918_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
    ]
