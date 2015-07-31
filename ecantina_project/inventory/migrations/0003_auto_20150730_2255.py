# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_comic_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='created',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='images',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='price',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='section',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='store',
        ),
    ]
