# Generated by Django 4.1.7 on 2023-05-14 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_worksorder_executor'),
        ('depositary', '0002_alter_depositary_options_depositary_date_closing_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositary',
            name='order',
        ),
        migrations.AddField(
            model_name='depositary',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.orders', verbose_name='Принадлежность к наряду'),
        ),
    ]
