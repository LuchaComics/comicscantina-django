# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151006_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(db_index=True, max_length=127),
        ),
        migrations.AlterField(
            model_name='customer',
            name='billing_phone',
            field=models.CharField(db_index=True, max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='billing_postal',
            field=models.CharField(db_index=True, max_length=31),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(unique=True, db_index=True, max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(db_index=True, max_length=63),
        ),
        migrations.AlterField(
            model_name='customer',
            name='joined',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(db_index=True, max_length=63),
        ),
        migrations.AlterField(
            model_name='customer',
            name='shipping_phone',
            field=models.CharField(db_index=True, max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='shipping_postal',
            field=models.CharField(db_index=True, max_length=31),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=511, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(db_index=True, max_digits=10, decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(db_index=True, related_name='product_tags', blank=True, to='api.Tag'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='created',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='has_finished',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='status',
            field=models.PositiveSmallIntegerField(db_index=True, choices=[(1, 'New Order'), (2, 'Picked'), (3, 'Shipped'), (4, 'Received'), (5, 'In-Store Sale'), (6, 'Online Sale')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], default=1),
        ),
    ]
