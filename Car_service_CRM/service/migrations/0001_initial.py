# Generated by Django 4.1.7 on 2023-04-03 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=50)),
                ('vin_number', models.CharField(max_length=17)),
                ('registration_number', models.CharField(max_length=14)),
                ('notes', models.TextField(blank=True)),
                ('date_start', models.DateTimeField(auto_now_add=True)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorksOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('standard', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(default='Согласование', max_length=20)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('completed', models.CharField(default='Не определено', max_length=30)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.orders')),
            ],
        ),
    ]
