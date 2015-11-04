# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcdbrand',
            name='images',
            field=models.ManyToManyField(to='api.GCDImage', blank=True),
        ),
        migrations.AlterField(
            model_name='gcdindiciapublisher',
            name='images',
            field=models.ManyToManyField(to='api.GCDImage', blank=True),
        ),
        migrations.AlterField(
            model_name='gcdissue',
            name='images',
            field=models.ManyToManyField(to='api.GCDImage', blank=True),
        ),
        migrations.AlterField(
            model_name='gcdpublisher',
            name='images',
            field=models.ManyToManyField(to='api.GCDImage', blank=True),
        ),
        migrations.AlterField(
            model_name='gcdseries',
            name='images',
            field=models.ManyToManyField(to='api.GCDImage', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='customers',
            field=models.ManyToManyField(to='api.Customer', blank=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='employees',
            field=models.ManyToManyField(to='api.Employee', blank=True),
        ),
    ]
