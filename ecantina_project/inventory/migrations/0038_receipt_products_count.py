# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_auto_20150820_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='products_count',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], default=0),
        ),
    ]
