# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150901_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 9, 1, 16, 33, 56, 678623)),
            preserve_default=False,
        ),
    ]
