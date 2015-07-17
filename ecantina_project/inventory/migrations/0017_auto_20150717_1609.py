# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20150717_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='comics',
            new_name='comic',
        ),
    ]
