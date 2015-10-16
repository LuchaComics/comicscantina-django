# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20151014_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='organization',
            field=models.ForeignKey(null=True, to='api.Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='store',
            field=models.ForeignKey(null=True, to='api.Store', blank=True),
        ),
    ]
