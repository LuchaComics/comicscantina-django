# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20151023_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 10, 24, 11, 47, 0, 627087)),
            preserve_default=False,
        ),
    ]
