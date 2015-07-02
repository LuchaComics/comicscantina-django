# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150702_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='friday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='friday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_open_wednesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='monday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='monday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='saturday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='saturday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='sunday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='sunday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='thursday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='thursday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='tuesday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='tuesday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='wednesday_from',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='store',
            name='wednesday_to',
            field=models.CharField(null=True, blank=True, max_length=7),
        ),
    ]
