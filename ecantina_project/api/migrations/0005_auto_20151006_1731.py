# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150929_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='city',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='country',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='postal',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='province',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='street_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='street_number',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='unit_number',
        ),
    ]
