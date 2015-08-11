# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20150810_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='receipt',
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_address',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_city',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_country',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_email',
            field=models.EmailField(null=True, max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_name',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_phone',
            field=models.CharField(null=True, max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_postal',
            field=models.CharField(null=True, max_length=31, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payer_province',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], choices=[(1, 'New Order'), (2, 'Picked'), (3, 'Shipped'), (4, 'Received'), (5, 'In-Store Sale'), (6, 'Online Sale')]),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
