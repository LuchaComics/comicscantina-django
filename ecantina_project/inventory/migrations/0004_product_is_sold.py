# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150730_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
