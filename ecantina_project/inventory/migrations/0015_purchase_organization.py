# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20150809_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='organization',
            field=models.ForeignKey(to='inventory.Organization', default=1),
            preserve_default=False,
        ),
    ]
