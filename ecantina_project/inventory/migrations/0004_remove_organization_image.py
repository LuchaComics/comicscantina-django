# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_organization_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='image',
        ),
    ]
