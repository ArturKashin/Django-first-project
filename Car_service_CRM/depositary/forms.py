from service.models import Orders
from .models import Depositary
from django.forms import ModelForm


# форма добавления деталей на склад
class DepositaryForm(ModelForm):
    class Meta:
        model = Depositary
        exclude = ['output_cost', 'order']


class DepositaryOwnerForm(ModelForm):
    class Meta:
        model = Depositary
        fields = ['order']

    # фильтр для добавления работ только в открытые наряды
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = Orders.objects.filter(date_completed__isnull=True)
        self.fields['order'].empty_label = 'Не зарезервирована'
