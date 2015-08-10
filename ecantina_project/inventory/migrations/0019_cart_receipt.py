# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20150809_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='receipt',
            field=models.ForeignKey(null=True, blank=True, to='inventory.Receipt'),
        ),
    ]
