# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20150811_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='billing_name',
            new_name='billing_first_name',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='shipping_name',
            new_name='billing_last_name',
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_first_name',
            field=models.CharField(blank=True, null=True, max_length=63),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_last_name',
            field=models.CharField(blank=True, null=True, max_length=63),
        ),
    ]
