# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_product_qrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcode'),
        ),
    ]
