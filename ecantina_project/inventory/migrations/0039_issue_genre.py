# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0038_receipt_products_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='genre',
            field=models.CharField(db_index=True, null=True, blank=True, max_length=255),
        ),
    ]
