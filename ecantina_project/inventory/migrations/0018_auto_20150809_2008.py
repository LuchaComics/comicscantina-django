# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20150809_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='city',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='country',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='email',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='has_custom_billing_address',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='postal',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='province',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='street_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='street_number',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='unit_number',
        ),
    ]
