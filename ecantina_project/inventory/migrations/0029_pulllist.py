# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_auto_20150818_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pulllist',
            fields=[
                ('pulllist_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=127)),
                ('customers', models.ManyToManyField(to='inventory.Customer')),
                ('organization', models.ForeignKey(to='inventory.Organization')),
                ('publisher', models.ForeignKey(to='inventory.Publisher')),
                ('series', models.ForeignKey(null=True, to='inventory.Series')),
                ('store', models.ForeignKey(to='inventory.Store')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'ec_pulllists',
            },
        ),
    ]
