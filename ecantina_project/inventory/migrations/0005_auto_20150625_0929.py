# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_organization_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='facebook_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='flickr_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='github_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='google_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='image',
        ),
        migrations.RemoveField(
            model_name='store',
            name='instagram_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='linkedin_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='twitter_url',
        ),
        migrations.RemoveField(
            model_name='store',
            name='youtube_url',
        ),
    ]
