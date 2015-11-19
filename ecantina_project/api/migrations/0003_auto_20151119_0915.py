# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='theme',
            field=models.CharField(choices=[('skin-1.css', 'Ligh Green'), ('skin-2.css', 'Aqua Green'), ('skin-3.css', 'Light Blue'), ('skin-4.css', 'Purple'), ('skin-5.css', 'Red'), ('skin-6.css', 'Black'), ('skin-7.css', 'Grey'), ('skin-8.css', 'Light Aqua Green'), ('skin-9.css', 'Yellow'), ('skin-10.css', 'Light Red'), ('skin-11.css', 'Dark Blue')], max_length=12, default='skin-5.css'),
        ),
        migrations.AddField(
            model_name='store',
            name='theme',
            field=models.CharField(choices=[('skin-1.css', 'Ligh Green'), ('skin-2.css', 'Aqua Green'), ('skin-3.css', 'Light Blue'), ('skin-4.css', 'Purple'), ('skin-5.css', 'Red'), ('skin-6.css', 'Black'), ('skin-7.css', 'Grey'), ('skin-8.css', 'Light Aqua Green'), ('skin-9.css', 'Yellow'), ('skin-10.css', 'Light Red'), ('skin-11.css', 'Dark Blue')], max_length=12, default='skin-5.css'),
        ),
    ]
