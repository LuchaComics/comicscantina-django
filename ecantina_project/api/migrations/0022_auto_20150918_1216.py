# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20150918_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='subject_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
