# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150702_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='joined',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_updated',
            field=models.DateTimeField(default='2015-07-01 13:19:19.965957-04', auto_now=True),
            preserve_default=False,
        ),
    ]
