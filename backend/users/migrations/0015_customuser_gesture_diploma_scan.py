# Generated by Django 3.2.6 on 2021-08-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210815_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gesture_diploma_scan',
            field=models.ImageField(blank=True, upload_to='gesture_diploma', verbose_name='Скан диплома о подготовке по жестовому языку'),
        ),
    ]
