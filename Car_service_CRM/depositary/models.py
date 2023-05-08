from django.db import models


class Depositary(models.Model):
    part_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул детали')
    part_name = models.CharField(max_length=300, verbose_name='Название детали')
    part_location = models.CharField(max_length=50, verbose_name='Расположение детали')
    input_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Входная стоимость')
    output_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name='Входная стоимость')
    markup_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Наценка %')
    quantity = models.IntegerField(default=1, verbose_name='Количество, шт.')