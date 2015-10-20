# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20151020_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='story',
            field=models.ForeignKey(to='api.GCDStory', null=True, blank=True),
        ),
    ]
