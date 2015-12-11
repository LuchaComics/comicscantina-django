# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_catalogitem_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='catalog',
            field=models.ForeignKey(null=True, to='api.CatalogItem', blank=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='issue',
            field=models.ForeignKey(null=True, to='api.GCDIssue', blank=True),
        ),
    ]
