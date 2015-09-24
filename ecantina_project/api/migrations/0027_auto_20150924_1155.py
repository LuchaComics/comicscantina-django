# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20150924_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='billing_email',
            new_name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='billing_email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='shipping_email',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='shipping_email',
        ),
    ]
