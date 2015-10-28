# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151028_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='wants_flyers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='wants_newsletter',
            field=models.BooleanField(default=False),
        ),
    ]
