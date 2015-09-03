# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150902_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='billing_email',
            field=models.EmailField(blank=True, null=True, max_length=254),
        ),
        migrations.AddField(
            model_name='customer',
            name='shipping_email',
            field=models.EmailField(blank=True, null=True, max_length=254),
        ),
    ]
