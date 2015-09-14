# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_comic_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='organization',
            field=models.ForeignKey(to='api.Organization', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comic',
            name='store',
            field=models.ForeignKey(to='api.Store', default=1),
            preserve_default=False,
        ),
    ]
