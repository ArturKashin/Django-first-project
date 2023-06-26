# Generated by Django 4.1.7 on 2023-06-25 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0008_alter_orders_options_alter_worksorder_executor'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='master',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Мастер приемщик'),
            preserve_default=False,
        ),
    ]