# Generated by Django 4.1.7 on 2023-04-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='client',
            field=models.CharField(max_length=50, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия наряда'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='date_start',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата открытия наряда'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='registration_number',
            field=models.CharField(max_length=14, verbose_name='Регистрационный номер А/М'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='vin_number',
            field=models.CharField(max_length=17, verbose_name='VIN номер'),
        ),
    ]
