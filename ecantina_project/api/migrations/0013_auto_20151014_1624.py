# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_emailsubscriber'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailSubscriber',
            new_name='EmailSubscription',
        ),
        migrations.RenameField(
            model_name='emailsubscription',
            old_name='subscriber_id',
            new_name='subscription_id',
        ),
        migrations.AlterModelTable(
            name='emailsubscription',
            table='ec_email_subscriptions',
        ),
    ]
