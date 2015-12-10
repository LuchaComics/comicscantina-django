# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_catalogitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='materials',
            field=models.CharField(blank=True, null=True, max_length=127),
        ),
    ]
