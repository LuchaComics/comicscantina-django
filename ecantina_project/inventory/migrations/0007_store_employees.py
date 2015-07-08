# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20150707_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='employees',
            field=models.ManyToManyField(to='inventory.Employee'),
        ),
    ]
