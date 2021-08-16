# Generated by Django 3.2.6 on 2021-08-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210816_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('step_1', 'Шаг 1'), ('step_2', 'Шаг 2'), ('step_3', 'Шаг 3'), ('step_4', 'Шаг 4'), ('step_5', 'Шаг 5'), ('step_6', 'Шаг 6'), ('on_check', 'Отправлена на проверку'), ('canceled', 'Отклонена'), ('confirmed', 'Успешно подтверждена'), ('completed', 'Завершена работа')], max_length=9, verbose_name='Статус заявки'),
        ),
    ]
