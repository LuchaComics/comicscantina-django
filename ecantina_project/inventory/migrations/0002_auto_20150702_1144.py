# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='store',
        ),
        migrations.AddField(
            model_name='employee',
            name='city',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='country',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='employee',
            name='phone',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='employee',
            name='postal',
            field=models.CharField(default='', max_length=31),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='province',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='street_name',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='street_number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='unit_number',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
    ]
