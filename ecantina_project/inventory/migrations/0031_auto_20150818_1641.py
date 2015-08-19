# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_remove_pulllist_store'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pulllist',
            options={'ordering': ('series',)},
        ),
        migrations.RemoveField(
            model_name='pulllist',
            name='name',
        ),
    ]
