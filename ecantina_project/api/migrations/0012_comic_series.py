# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_receipt_products_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='series',
            field=models.ForeignKey(to='api.GCDSeries', default=1),
            preserve_default=False,
        ),
    ]
