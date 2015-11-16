# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_customer_is_shipping_same_as_billing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='billing_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='shipping_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='billing_name',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='shipping_name',
        ),
    ]
