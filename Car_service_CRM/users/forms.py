from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person


# регистрация сотрудника
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']
        labels = {'first_name': 'Полное имя'}
