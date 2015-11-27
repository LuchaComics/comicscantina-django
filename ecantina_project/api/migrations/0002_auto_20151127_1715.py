# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdomain',
            name='name',
            field=models.CharField(unique=True, null=True, max_length=127, db_index=True, blank=True),
        ),
    ]
