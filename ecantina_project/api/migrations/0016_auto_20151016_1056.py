# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151016_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='billing_first_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='billing_last_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='shipping_first_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='shipping_last_name',
        ),
        migrations.AddField(
            model_name='receipt',
            name='billing_name',
            field=models.CharField(blank=True, null=True, max_length=126),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_name',
            field=models.CharField(blank=True, null=True, max_length=126),
        ),
    ]
