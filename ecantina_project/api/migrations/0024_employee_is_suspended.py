# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20150921_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
    ]
