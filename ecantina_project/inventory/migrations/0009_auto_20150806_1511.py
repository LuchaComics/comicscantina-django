# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150806_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='country',
            field=models.ForeignKey(null=True, default=250, to='inventory.Country'),
        ),
    ]
