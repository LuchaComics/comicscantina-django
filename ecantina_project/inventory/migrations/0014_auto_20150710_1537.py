# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_customer_has_consented'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='product_id',
            new_name='comic_id',
        ),
        migrations.AlterField(
            model_name='comic',
            name='section',
            field=models.ForeignKey(default=1, to='inventory.Section'),
            preserve_default=False,
        ),
    ]
