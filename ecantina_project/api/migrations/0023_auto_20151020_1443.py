# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20151019_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='paypal_email',
            field=models.EmailField(default='bart@mikasoftware.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='store',
            name='paypal_email',
            field=models.EmailField(default='bart@mikasoftware.com', max_length=254),
            preserve_default=False,
        ),
    ]
