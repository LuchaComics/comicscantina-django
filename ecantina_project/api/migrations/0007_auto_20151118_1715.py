# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_imagebinary'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBinaryUpload',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('created', models.DateField(null=True, auto_now=True)),
                ('file_type', models.CharField(max_length=4, db_index=True, choices=[('png', 'Portable Network Graphics (PNG)'), ('jpeg', 'Joint Photographic Experts Group picture (JPEG'), ('jpg', 'Joint Photographic Experts Group picture (JPG'), ('bmp', 'Bitmap Image File (BMP'), ('tiff', 'Tagged Image File Format (TIFF'), ('gif', 'Graphics Interchange Format (GIF')])),
                ('mime_type', models.CharField(max_length=15, db_index=True, default='image/jpeg', choices=[('image/png', 'PNG'), ('image/jpeg', 'JPEG/JPG'), ('image/bmp', 'BMP'), ('image/tiff', 'TIFF'), ('image/gif', 'GIF')])),
                ('data', models.BinaryField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'ec_image_binary_uploads',
            },
        ),
        migrations.DeleteModel(
            name='ImageBinary',
        ),
    ]
