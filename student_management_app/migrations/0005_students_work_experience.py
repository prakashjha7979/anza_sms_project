# Generated by Django 4.0.1 on 2022-01-25 05:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_auto_20220119_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='work_experience',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
