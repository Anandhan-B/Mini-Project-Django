# Generated by Django 4.2.4 on 2023-09-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0029_alter_faqsection_ans'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloginstat',
            name='logout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userloginstat',
            name='session_id',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
