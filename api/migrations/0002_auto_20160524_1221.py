# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='cgc_rating',
            field=models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], choices=[(10.0, '10.0 Gem Mint'), (9.9, '9.9 Mint'), (9.8, '9.8 Near Mint/Mint'), (9.6, '9.6 Near Mint +'), (9.4, '9.4 Near Mint'), (9.2, '9.2 Near Mint -'), (9.0, '9.0 Very Fine/Near Mint'), (8.5, '8.5 Very Fine +'), (8.0, '8.0 Very Fine'), (7.5, '7.5 Very Fine -'), (7.0, '7.0 Fine/Very Fine'), (6.5, '6.5 Fine +'), (6.0, '6.0 Fine'), (5.5, '5.5 Fine -'), (5.0, '5.0 Very Good/Fine'), (4.5, '4.5 Very Good +'), (4.0, '4.0 Very Good'), (3.5, '3.5 Very Good -'), (3.0, '3.0 Good/Very Good'), (2.5, '2.5 Good +'), (2.0, '2.0 Good'), (1.8, '1.8 Good -'), (1.5, '1.5 Fair/Good'), (1.0, '1.0 Fair'), (0.5, '.5 Poor'), (0, 'NG')]),
        ),
        migrations.AlterField(
            model_name='comic',
            name='label_colour',
            field=models.CharField(max_length=63, blank=True, choices=[('Yellow', 'CGC Yellow Label'), ('Blue', 'CGC Blue Label'), ('Purple', 'CGC Purple Label'), ('Red', 'CGC Red Label'), ('cbcs', 'CBCS'), ('pgx', 'PGX')], null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD'), (484, 'MXN')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD'), (484, 'MXN')]),
        ),
        migrations.AlterField(
            model_name='store',
            name='currency',
            field=models.PositiveSmallIntegerField(default=124, choices=[(124, 'CAD'), (840, 'USD'), (484, 'MXN')]),
        ),
    ]
