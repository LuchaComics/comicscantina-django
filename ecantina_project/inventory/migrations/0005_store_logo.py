# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150702_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='logo',
            field=models.ForeignKey(to='inventory.ImageUpload', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
