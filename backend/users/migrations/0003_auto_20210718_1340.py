# Generated by Django 3.2.5 on 2021-07-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210531_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='passport_part1_scan_url',
            field=models.ImageField(blank=True, upload_to='passport_part1'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='passport_part2_scan_url',
            field=models.ImageField(blank=True, upload_to='passport_part2'),
        ),
    ]
