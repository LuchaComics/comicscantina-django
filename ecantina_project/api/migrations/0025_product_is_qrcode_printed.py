# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_employee_is_suspended'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_qrcode_printed',
            field=models.BooleanField(default=False),
        ),
    ]
