# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0010_imageupload_is_assigned'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('joined', models.DateField(null=True, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=63)),
                ('last_name', models.CharField(max_length=63)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('street_name', models.CharField(max_length=63)),
                ('street_number', models.CharField(max_length=15)),
                ('unit_number', models.CharField(max_length=15, null=True, blank=True)),
                ('city', models.CharField(max_length=63)),
                ('province', models.CharField(max_length=63)),
                ('country', models.CharField(max_length=63)),
                ('postal', models.CharField(max_length=31)),
                ('profile', models.ForeignKey(null=True, to='inventory.ImageUpload', blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'db_table': 'ec_customers',
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='customers',
            field=models.ManyToManyField(to='inventory.Customer'),
        ),
    ]
