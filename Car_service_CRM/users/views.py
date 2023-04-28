from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
# форма авторизации пользователя
from django.contrib.auth.forms import AuthenticationForm
from .models import Person
from .serializers import UserSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create your views here.
def register_user(request):
    person = Person.objects.get(user=request.user)
    if request.method == "POST":
        form_user = UserForm(request.POST)
        if form_user.is_valid():
            user = form_user.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            person = Person.objects.get(user=request.user)
            person.jod_title = request.POST.get('jod_title')
            person.save()
            return redirect('index')
        else:
            pass

    context = {'form_user': UserForm(), 'person': person}
    return render(request, 'users/register_user.html', context)


# авторизация
def loginuser(request):
    if request.method == "GET":
        context = {'form': AuthenticationForm()}
        return render(request, 'service/loginuser.html', context)
    else:
        user = authenticate(request, username=request.POST['username'].lower(), password=request.POST['password'])
        if user is None:
            context = {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'}
            return render(request, 'service/loginuser.html', context)
        else:
            login(request, user)
            if Person.objects.filter(user=request.user, jod_title="Мастер"):
                return redirect('index')
            if Person.objects.filter(user=request.user, jod_title="Механик"):
                return redirect('order-for-mechanical')


# выход из акк
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')