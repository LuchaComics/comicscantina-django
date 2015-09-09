# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_gcdissue_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcdissue',
            name='product_name',
            field=models.CharField(max_length=511, blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=511, blank=True, null=True),
        ),
    ]
