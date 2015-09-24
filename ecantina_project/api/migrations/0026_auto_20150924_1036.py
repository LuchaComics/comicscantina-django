# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_product_is_qrcode_printed'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='language',
            field=models.CharField(default='EN', choices=[('EN', 'English')], max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD')]),
        ),
        migrations.AddField(
            model_name='product',
            name='language',
            field=models.CharField(default='EN', choices=[('EN', 'English')], max_length=2),
        ),
        migrations.AddField(
            model_name='store',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD')]),
        ),
        migrations.AddField(
            model_name='store',
            name='language',
            field=models.CharField(default='EN', choices=[('EN', 'English')], max_length=2),
        ),
    ]
