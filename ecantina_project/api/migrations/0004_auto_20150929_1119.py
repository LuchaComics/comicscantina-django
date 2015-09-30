# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150925_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='subject_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
