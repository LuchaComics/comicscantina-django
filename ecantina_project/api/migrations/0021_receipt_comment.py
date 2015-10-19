# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20151019_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='comment',
            field=models.CharField(null=True, max_length=511, blank=True),
        ),
    ]
