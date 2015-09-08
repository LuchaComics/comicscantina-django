# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20150903_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='gcdissue',
            name='product_name',
            field=models.CharField(blank=True, db_index=True, null=True, max_length=255),
        ),
    ]
