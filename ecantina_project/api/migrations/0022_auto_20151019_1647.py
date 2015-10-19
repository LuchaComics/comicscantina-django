# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_receipt_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='comment',
            field=models.CharField(default='', max_length=511, null=True, blank=True),
        ),
    ]
