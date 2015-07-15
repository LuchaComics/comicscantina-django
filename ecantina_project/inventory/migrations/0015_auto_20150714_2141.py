# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20150710_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='created',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='comic',
            name='last_updated',
            field=models.DateTimeField(default='2015-01-01', auto_now=True),
            preserve_default=False,
        ),
    ]
