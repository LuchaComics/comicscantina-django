# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_pulllist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pulllist',
            name='store',
        ),
    ]
