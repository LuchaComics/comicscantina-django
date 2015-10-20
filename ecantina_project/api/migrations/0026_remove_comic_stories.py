# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20151020_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='stories',
        ),
    ]
