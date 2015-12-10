# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogItem',
            fields=[
                ('catalog_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127, db_index=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Comic'), (2, 'Furniture'), (3, 'Coin')], db_index=True, default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('description', models.TextField(blank=True, default='')),
                ('brand_name', models.CharField(max_length=127, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('length_in_meters', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('width_in_meters', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('height_in_meters', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('weight_in_kilograms', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('volume_in_litres', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('materials', models.CharField(max_length=127, db_index=True)),
                ('is_tangible', models.BooleanField(default=True)),
                ('is_flammable', models.BooleanField(default=False)),
                ('is_biohazard', models.BooleanField(default=False)),
                ('is_toxic', models.BooleanField(default=False)),
                ('is_explosive', models.BooleanField(default=False)),
                ('is_corrosive', models.BooleanField(default=False)),
                ('is_volatile', models.BooleanField(default=False)),
                ('is_radioactive', models.BooleanField(default=False)),
                ('is_restricted', models.BooleanField(default=False)),
                ('restrictions', models.TextField(blank=True, default='')),
                ('image', models.ForeignKey(null=True, blank=True, to='api.ImageUpload')),
                ('organization', models.ForeignKey(to='api.Organization')),
            ],
            options={
                'db_table': 'ec_catalog_items',
                'ordering': ('name',),
            },
        ),
    ]
