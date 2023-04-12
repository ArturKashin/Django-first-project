from django.db import models
from django.contrib.auth.models import User


class Orders(models.Model):
    client = models.CharField(max_length=50, verbose_name='Клиент')
    vin_number = models.CharField(max_length=17, verbose_name='VIN номер')
    registration_number = models.CharField(max_length=14, verbose_name='Регистрационный номер А/М')
    notes = models.TextField(null=True, blank=True, verbose_name='Комментарии')
    date_start = models.DateTimeField(auto_now_add=True, verbose_name='Дата открытия наряда')
    date_completed = models.DateTimeField(null=True, blank=True, verbose_name='Дата закрытия наряда')

    def __str__(self):
        return f"{self.client} А/М - {self.registration_number}"


class WorksOrder(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование работы')
    standard = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Норма времени н/ч')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость н/ч')
    order_status = models.CharField(default='Согласование', max_length=20, verbose_name='Статус работы')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Выбор з/наряда')
    completed = models.CharField(max_length=30, default='Не определено', verbose_name='Исполнитель')

    def __str__(self):
        return f"{self.order} -->> {self.name}"

