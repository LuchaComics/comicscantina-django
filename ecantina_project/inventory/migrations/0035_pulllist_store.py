# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0034_auto_20150819_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='pulllist',
            name='store',
            field=models.ForeignKey(default=1, to='inventory.Store'),
            preserve_default=False,
        ),
    ]
