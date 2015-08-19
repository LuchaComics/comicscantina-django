# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_auto_20150818_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pulllist',
            name='publisher',
        ),
    ]
