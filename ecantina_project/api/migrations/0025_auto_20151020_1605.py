# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_comic_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='story',
        ),
        migrations.AddField(
            model_name='comic',
            name='stories',
            field=models.ManyToManyField(to='api.GCDStory'),
        ),
    ]
