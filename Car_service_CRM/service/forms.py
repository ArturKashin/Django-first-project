from django.forms import ModelForm
from django import forms

from users.models import Person
from .models import Orders, WorksOrder
from django.contrib.auth.models import User


# форма добавления наряда
class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['client',
                  'vin_number',
                  'registration_number',
                  'notes',
                  ]
        widgets = {'notes': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input col-12'})


# форма добавления работ к наряду
class WorksForm(ModelForm):
    class Meta:
        model = WorksOrder
        fields = ['name', 'standard', 'price', 'executor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].empty_label = 'Исполнитель не выбран'

        # выбор executor только механик
        users = Person.objects.filter(jod_title='Механик')
        id_mechanic = []
        for user in users:
            id_mechanic.append(user.user.id)
        self.fields['executor'].queryset = User.objects.filter(id__in=id_mechanic)
