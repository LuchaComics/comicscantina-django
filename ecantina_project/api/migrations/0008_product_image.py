# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150827_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ForeignKey(blank=True, to='api.ImageUpload', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
