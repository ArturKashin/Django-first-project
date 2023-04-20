from django.db import models
from django.contrib.auth.models import User


# профиль сотрудника
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name='Имя')
    time = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Выработка н/ч')
    jod_title = models.CharField(max_length=20, default='Механик', verbose_name='Должность')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата трудоустройства')

    def __str__(self):
        return f"{self.name}, {self.jod_title}"
