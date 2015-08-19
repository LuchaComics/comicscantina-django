# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0033_auto_20150819_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='pulllistsubscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 8, 19, 10, 16, 35, 635219)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pulllistsubscription',
            name='organization',
            field=models.ForeignKey(to='inventory.Organization', default=1),
            preserve_default=False,
        ),
    ]
