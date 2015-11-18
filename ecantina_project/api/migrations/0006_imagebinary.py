# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151116_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBinary',
            fields=[
                ('id', models.AutoField(primary_key=True, db_index=True, serialize=False)),
                ('data', models.BinaryField()),
            ],
            options={
                'db_table': 'ec_image_binaries',
            },
        ),
    ]
