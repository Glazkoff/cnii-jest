# Generated by Django 3.2.5 on 2021-07-18 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210718_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='passport_part1_scan_url',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='passport_part2_scan_url',
        ),
        migrations.AddField(
            model_name='customuser',
            name='passport_part1_scan',
            field=models.ImageField(blank=True, upload_to='passport_part1', verbose_name='Скан паспорта (часть 1)'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='passport_part2_scan',
            field=models.ImageField(blank=True, upload_to='passport_part2', verbose_name='Скан паспорта (часть 2)'),
        ),
    ]
