# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151006_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='error',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], choices=[(0, 'No Error'), (1, 'Cancelled Online Order')]),
        ),
        migrations.AddField(
            model_name='receipt',
            name='has_error',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
