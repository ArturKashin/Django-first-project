from django.db import models
from service.models import Orders


class Depositary(models.Model):
    part_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул детали')
    part_name = models.CharField(max_length=300, verbose_name='Название детали')
    part_location = models.CharField(max_length=50, verbose_name='Расположение детали')
    input_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Входная стоимость')
    output_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name='Выходная стоимость')
    markup_cost = models.DecimalField(max_digits=10, decimal_places=2, default=5, verbose_name='Наценка %')
    quantity = models.IntegerField(default=1, verbose_name='Количество, шт.')
    date_opening = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата поступления')
    date_closing = models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Принадлежность к наряду')

    def __str__(self):
        return f"{self.part_name}"

    class Meta:
        ordering = ['-id']
