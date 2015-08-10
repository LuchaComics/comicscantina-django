# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20150810_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receipt',
            options={'ordering': ('last_updated',)},
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='purchased_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='type',
        ),
        migrations.AddField(
            model_name='receipt',
            name='employee',
            field=models.ForeignKey(null=True, to='inventory.Employee', blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='has_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='has_purchased_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='has_tax',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 8, 10, 14, 44, 5, 348236)),
            preserve_default=False,
        ),
    ]
