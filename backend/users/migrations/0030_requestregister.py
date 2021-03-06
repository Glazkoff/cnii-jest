# Generated by Django 3.2.6 on 2021-08-30 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20210830_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='Порядковый номер')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='users.request', verbose_name='Заявка')),
            ],
        ),
    ]
