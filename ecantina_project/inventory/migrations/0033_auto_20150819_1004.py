# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0032_remove_pulllist_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='PulllistSubscription',
            fields=[
                ('subscription_id', models.AutoField(serialize=False, primary_key=True)),
                ('copies', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('customer', models.ForeignKey(to='inventory.Customer')),
            ],
            options={
                'db_table': 'ec_pulllists_subscriptions',
            },
        ),
        migrations.RemoveField(
            model_name='pulllist',
            name='customers',
        ),
        migrations.AddField(
            model_name='pulllistsubscription',
            name='pulllist',
            field=models.ForeignKey(to='inventory.Pulllist'),
        ),
    ]
