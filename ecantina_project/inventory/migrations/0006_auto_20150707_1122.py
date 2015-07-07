# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_store_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='location',
            name='store',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='location',
        ),
        migrations.RemoveField(
            model_name='section',
            name='location',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
