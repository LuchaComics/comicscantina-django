# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20150811_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_address',
            new_name='billing_address',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_city',
            new_name='billing_city',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_country',
            new_name='billing_country',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_email',
            new_name='billing_email',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_name',
            new_name='billing_name',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_phone',
            new_name='billing_phone',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_postal',
            new_name='billing_postal',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='payer_province',
            new_name='billing_province',
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_address',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_city',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_country',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_email',
            field=models.EmailField(null=True, max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_name',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_phone',
            field=models.CharField(null=True, max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_postal',
            field=models.CharField(null=True, max_length=31, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='shipping_province',
            field=models.CharField(null=True, max_length=63, blank=True),
        ),
    ]
