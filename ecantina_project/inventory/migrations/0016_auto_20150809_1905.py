# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_purchase_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('receipt_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchased_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)], choices=[(1, 'Store'), (2, 'Online')], default=1)),
                ('payment_method', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)], choices=[(1, 'Cash'), (2, 'Debit Card'), (3, 'Credit Card'), (4, 'Gift Card'), (5, 'Store Points'), (6, 'Cheque'), (7, 'PayPal'), (8, 'Invoice'), (9, 'Other')], default=1)),
                ('has_custom_billing_address', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=63, null=True, blank=True)),
                ('last_name', models.CharField(max_length=63, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('street_name', models.CharField(max_length=63, null=True, blank=True)),
                ('street_number', models.CharField(max_length=15, null=True, blank=True)),
                ('unit_number', models.CharField(max_length=15, null=True, blank=True)),
                ('city', models.CharField(max_length=63, null=True, blank=True)),
                ('province', models.CharField(max_length=63, null=True, blank=True)),
                ('country', models.CharField(max_length=63, null=True, blank=True)),
                ('postal', models.CharField(max_length=31, null=True, blank=True)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10, default=0.0)),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=10, default=0.0)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, default=0.0)),
                ('customer', models.ForeignKey(to='inventory.Customer', blank=True, null=True)),
                ('organization', models.ForeignKey(to='inventory.Organization')),
            ],
            options={
                'db_table': 'ec_receipts',
                'ordering': ('purchased_date',),
            },
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='country',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='type',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='customer',
            field=models.ForeignKey(to='inventory.Customer', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='purchases',
            field=models.ManyToManyField(to='inventory.Purchase'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='store',
            field=models.ForeignKey(to='inventory.Store'),
        ),
    ]
