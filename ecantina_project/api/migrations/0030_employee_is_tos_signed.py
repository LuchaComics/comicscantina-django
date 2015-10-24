# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_wishlist_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_tos_signed',
            field=models.BooleanField(default=False),
        ),
    ]
