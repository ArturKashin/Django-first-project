# Generated by Django 4.1.7 on 2023-04-16 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='jod_title',
            field=models.CharField(blank=True, choices=[(1, 'Мастер'), (2, 'Механик')], max_length=20, null=True, verbose_name='Должность'),
        ),
    ]
