# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_product_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='organization',
        ),
    ]
