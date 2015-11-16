# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151116_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='customer',
            field=models.ForeignKey(null=True, to='api.Customer', blank=True),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='employee',
            field=models.ForeignKey(null=True, to='api.Employee', blank=True),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='organization',
            field=models.ForeignKey(null=True, to='api.Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='store',
            field=models.ForeignKey(null=True, to='api.Store', blank=True),
        ),
    ]
