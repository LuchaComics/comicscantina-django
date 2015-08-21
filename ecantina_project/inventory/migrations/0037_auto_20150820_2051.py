# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0036_auto_20150820_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='receipt',
            field=models.ForeignKey(null=True, blank=True, to='inventory.Receipt'),
        ),
    ]
