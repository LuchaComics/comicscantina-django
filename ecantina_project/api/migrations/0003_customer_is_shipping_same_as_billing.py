# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151103_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_shipping_same_as_billing',
            field=models.BooleanField(default=False),
        ),
    ]
