# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151119_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='theme',
            new_name='style',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='theme',
            new_name='style',
        ),
    ]
