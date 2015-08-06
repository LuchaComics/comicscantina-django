# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20150806_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='country',
            field=models.ForeignKey(null=True, default=37, to='inventory.Country'),
        ),
    ]
