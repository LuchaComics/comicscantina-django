# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='customer',
            name='verification_key',
            field=models.CharField(default='', blank=True, max_length=63),
        ),
        migrations.AlterField(
            model_name='employee',
            name='verification_key',
            field=models.CharField(default='', blank=True, max_length=63),
        ),
    ]
