# Generated by Django 4.2.4 on 2023-09-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0028_faqsection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqsection',
            name='ans',
            field=models.CharField(max_length=1000),
        ),
    ]
