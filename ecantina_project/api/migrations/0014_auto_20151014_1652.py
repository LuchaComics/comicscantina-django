# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20151014_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsubscription',
            name='email',
            field=models.EmailField(max_length=254, unique=True, db_index=True),
        ),
    ]
