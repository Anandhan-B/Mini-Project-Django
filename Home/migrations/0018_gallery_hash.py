# Generated by Django 4.2.4 on 2023-08-31 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0017_alter_gallery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='hash',
            field=models.CharField(default=1, max_length=32, unique=True),
            preserve_default=False,
        ),
    ]
