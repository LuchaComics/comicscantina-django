# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20150709_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='has_consented',
            field=models.BooleanField(default=False),
        ),
    ]
