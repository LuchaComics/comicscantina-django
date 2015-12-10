# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151210_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogitem',
            name='store',
            field=models.ForeignKey(to='api.Store', default=1),
            preserve_default=False,
        ),
    ]
