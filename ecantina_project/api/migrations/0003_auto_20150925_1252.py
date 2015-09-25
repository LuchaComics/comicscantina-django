# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150925_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_coins_vendor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_comics_vendor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='store',
            name='is_furniture_vendor',
            field=models.BooleanField(default=False),
        ),
    ]
