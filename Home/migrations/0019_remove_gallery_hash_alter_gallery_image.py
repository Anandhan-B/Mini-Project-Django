# Generated by Django 4.2.4 on 2023-08-31 17:27

import Home.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0018_gallery_hash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='hash',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(storage=Home.storage.NoRenameStorageForModel(), unique=True, upload_to='images/'),
        ),
    ]
