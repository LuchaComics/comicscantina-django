# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_pulllist_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='publisher_name',
            field=models.CharField(db_index=True, max_length=255, default='Mika Software'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='publisher_name',
            field=models.CharField(db_index=True, max_length=255, default='Mika Software'),
            preserve_default=False,
        ),
    ]
