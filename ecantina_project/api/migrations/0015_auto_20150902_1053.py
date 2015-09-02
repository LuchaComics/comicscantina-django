# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_comic_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='series',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='store',
        ),
    ]
