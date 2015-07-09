# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_helprequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='is_assigned',
            field=models.BooleanField(default=False),
        ),
    ]
