# Generated by Django 4.1.7 on 2023-04-16 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_orders_final_price_alter_worksorder_final_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksorder',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость ч/руб.'),
        ),
    ]