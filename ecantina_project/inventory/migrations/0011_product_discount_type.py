# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20150809_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, '%'), (2, '$')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
