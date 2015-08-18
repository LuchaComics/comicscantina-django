# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20150818_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='billing_name',
            field=models.CharField(max_length=126, default='Bartlomiej Mika'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_name',
            field=models.CharField(max_length=126, default='Bartlomiej Mika'),
            preserve_default=False,
        ),
    ]
