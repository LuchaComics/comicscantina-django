# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_employee_is_tos_signed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_tos_signed',
            field=models.BooleanField(default=False),
        ),
    ]
