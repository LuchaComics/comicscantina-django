# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_product_has_no_shipping'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSubscriber',
            fields=[
                ('subscriber_id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(null=True, blank=True, to='api.Organization')),
                ('store', models.ForeignKey(null=True, blank=True, to='api.Store')),
            ],
            options={
                'db_table': 'ec_email_subscribers',
                'ordering': ('submission_date',),
            },
        ),
    ]
