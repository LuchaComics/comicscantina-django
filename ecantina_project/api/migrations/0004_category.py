# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_brand_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_id', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'ec_categories',
                'ordering': ('name',),
            },
        ),
    ]
