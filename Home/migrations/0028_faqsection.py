# Generated by Django 4.2.4 on 2023-09-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0027_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='faqsection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.CharField(max_length=200)),
                ('ans', models.CharField(max_length=500)),
            ],
        ),
    ]