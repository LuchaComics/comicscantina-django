# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_store_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Owner'), (1, 'Manager'), (2, 'Worker')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
        ),
    ]
