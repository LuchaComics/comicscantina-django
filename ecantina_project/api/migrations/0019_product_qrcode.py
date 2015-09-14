# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150909_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qrcode',
            field=models.ImageField(upload_to='qrcode', null=True, blank=True),
        ),
    ]
