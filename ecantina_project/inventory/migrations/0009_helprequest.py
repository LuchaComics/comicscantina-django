# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150709_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('help_id', models.AutoField(serialize=False, primary_key=True)),
                ('subject', models.PositiveSmallIntegerField(choices=[(1, 'Feedback'), (2, 'Error'), (3, 'Checkout'), (4, 'Inventory'), (5, 'Pull List'), (6, 'Sales'), (7, 'Emailing List'), (8, 'Store Settings / Users'), (9, 'Dashboard')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], default=1)),
                ('subject_url', models.URLField(null=True, blank=True)),
                ('message', models.TextField(null=True)),
                ('submission_date', models.DateField(auto_now=True, null=True)),
                ('employee', models.ForeignKey(to='inventory.Employee')),
                ('organization', models.ForeignKey(to='inventory.Organization')),
                ('screenshot', models.ForeignKey(null=True, blank=True, to='inventory.ImageUpload')),
                ('store', models.ForeignKey(to='inventory.Store')),
            ],
            options={
                'db_table': 'ec_help_requests',
                'ordering': ('submission_date',),
            },
        ),
    ]
