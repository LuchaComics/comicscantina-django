# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_receipt_purchased'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgShippingPreference',
            fields=[
                ('shipping_pref_id', models.AutoField(serialize=False, primary_key=True)),
                ('is_pickup_only', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(to='api.Organization')),
            ],
            options={
                'db_table': 'ec_org_shipping_preferences',
                'ordering': ('organization',),
            },
        ),
        migrations.CreateModel(
            name='OrgShippingRate',
            fields=[
                ('shipping_rate_id', models.AutoField(serialize=False, primary_key=True)),
                ('country', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(840)], choices=[(124, 'Canada'), (840, 'United States'), (484, 'Mexico')], blank=True)),
                ('comics_rate1', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate2', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate3', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate4', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate5', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate6', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate7', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate8', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate9', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate10', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('organization', models.ForeignKey(to='api.Organization')),
            ],
            options={
                'db_table': 'ec_org_shipping_rates',
                'ordering': ('country',),
            },
        ),
        migrations.CreateModel(
            name='StoreShippingPreference',
            fields=[
                ('shipping_pref_id', models.AutoField(serialize=False, primary_key=True)),
                ('is_pickup_only', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(to='api.Organization')),
            ],
            options={
                'db_table': 'ec_store_shipping_preferences',
                'ordering': ('organization',),
            },
        ),
        migrations.CreateModel(
            name='StoreShippingRate',
            fields=[
                ('shipping_rate_id', models.AutoField(serialize=False, primary_key=True)),
                ('country', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(840)], choices=[(124, 'Canada'), (840, 'United States'), (484, 'Mexico')], blank=True)),
                ('comics_rate1', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate2', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate3', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate4', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate5', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate6', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate7', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate8', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate9', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('comics_rate10', models.DecimalField(default=0.0, db_index=True, decimal_places=2, max_digits=10)),
                ('organization', models.ForeignKey(to='api.Organization')),
                ('store', models.ForeignKey(to='api.Store')),
            ],
            options={
                'db_table': 'ec_store_shipping_rates',
                'ordering': ('country',),
            },
        ),
        migrations.AddField(
            model_name='storeshippingpreference',
            name='rates',
            field=models.ManyToManyField(related_name='store_shipping_rates', blank=True, db_index=True, to='api.StoreShippingRate'),
        ),
        migrations.AddField(
            model_name='storeshippingpreference',
            name='store',
            field=models.ForeignKey(to='api.Store'),
        ),
        migrations.AddField(
            model_name='orgshippingpreference',
            name='rates',
            field=models.ManyToManyField(related_name='ord_shipping_rates', blank=True, db_index=True, to='api.OrgShippingRate'),
        ),
    ]
