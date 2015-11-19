# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151119_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='theme',
            field=models.CharField(default='ecantina-style-5.css', choices=[('ecantina-style-0.css', 'Green'), ('ecantina-style-1.css', 'Ligh Green'), ('ecantina-style-2.css', 'Aqua Green'), ('ecantina-style-3.css', 'Blue'), ('ecantina-style-4.css', 'Purple'), ('ecantina-style-5.css', 'Red'), ('ecantina-style-6.css', 'Black'), ('ecantina-style-7.css', 'Grey'), ('ecantina-style-8.css', 'Light Aqua Green'), ('ecantina-style-9.css', 'Yellow'), ('ecantina-style-10.css', 'Light Red'), ('ecantina-style-11.css', 'Dark Blue')], max_length=31),
        ),
        migrations.AlterField(
            model_name='store',
            name='theme',
            field=models.CharField(default='ecantina-style-5.css', choices=[('ecantina-style-0.css', 'Green'), ('ecantina-style-1.css', 'Ligh Green'), ('ecantina-style-2.css', 'Aqua Green'), ('ecantina-style-3.css', 'Blue'), ('ecantina-style-4.css', 'Purple'), ('ecantina-style-5.css', 'Red'), ('ecantina-style-6.css', 'Black'), ('ecantina-style-7.css', 'Grey'), ('ecantina-style-8.css', 'Light Aqua Green'), ('ecantina-style-9.css', 'Yellow'), ('ecantina-style-10.css', 'Light Red'), ('ecantina-style-11.css', 'Dark Blue')], max_length=31),
        ),
    ]
