from django.forms import ModelForm
from .models import Orders, WorksOrder


# форма добавления наряда
class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['client',
                  'vin_number',
                  'registration_number',
                  'notes',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input col-12'})


# форма добавления работ к наряду
class WorksForm(ModelForm):
    class Meta:
        model = WorksOrder
        fields = ['name', 'standard', 'price']


    # фильтр для добавления работ только в открытые наряды
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['order'].queryset = Orders.objects.filter(date_completed__isnull=True)
