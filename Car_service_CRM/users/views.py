from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from depositary.utils import master_access
from service.models import Orders, WorksOrder
from service.utils import paginator_order
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
# форма авторизации пользователя
from django.contrib.auth.forms import AuthenticationForm
from .models import Person
from .utils import search_worker_order
from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


@login_required(login_url='loginuser')
@master_access
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
@login_required(login_url='loginuser')
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')


# список работников
@login_required(login_url='loginuser')
@master_access
def view_workers(request):
    person = Person.objects.get(user=request.user)
    workers = Person.objects.all()
    context = {
        'person': person,
        'workers': workers,
    }
    return render(request, 'users/workers.html', context)


# просмотреть работника
@login_required(login_url='loginuser')
@master_access
def view_worker(request, pk):
    global orders
    person = Person.objects.get(user=request.user)
    worker = Person.objects.get(id=pk)
    works = WorksOrder.objects.filter(executor=worker.user)

    # поиск нарядов, в которых были выполнены работы
    sort_work = []
    for work in works:
        if work.order.id not in sort_work:
            sort_work.append(work.order.id)

    # ручной поиск
    if request.method == "GET":
        search_query = request.GET.get('search', '')
        start_date = request.GET.get('start-date', '')
        end_date = request.GET.get('end-date', '')

        orders = search_worker_order(sort_work, search_query, start_date, end_date)
        orders = paginator_order(request, orders)

    # подсчет норм/часов в наряде
    production = {}
    for work in works:
        if work.order.id in production:
            production[work.order.id] += work.standard
        else:
            production[work.order.id] = work.standard

    # подсчет выработки норм час
    production_employee = 0
    production_works = WorksOrder.objects.filter(order__in=orders)
    for pw in production_works:
        production_employee += pw.standard

    context = {
        'person': person,
        'worker': worker,
        'works': works,
        'orders': orders,
        'production': production,
        'production_employee': production_employee,
    }
    return render(request, 'users/worker.html', context)


# просмотреть мастера
@login_required(login_url='loginuser')
@master_access
def view_master(request, pk):
    if request.method == "GET":
        person = Person.objects.get(user=request.user)
        master = Person.objects.get(id=pk)
        order_s = Orders.objects.filter(master=master.user)

        search_query = request.GET.get('search', '')
        start_date = request.GET.get('start-date', '')
        end_date = request.GET.get('end-date', '')
        order_s = search_worker_order(order_s, search_query, start_date, end_date)
        order_s = paginator_order(request, order_s)

        # подсчет норм/часов в наряде
        works = WorksOrder.objects.filter(order__in=order_s)
        production = {}
        for work in works:
            if work.order.id in production:
                production[work.order.id] += work.standard
            else:
                production[work.order.id] = work.standard

        for order in order_s:
            if order.id not in production:
                production[order.id] = 0

        # подсчет выработки норм час
        production_employee = 0
        production_works = WorksOrder.objects.filter(order__in=order_s)
        for pw in production_works:
            production_employee += pw.standard

        context = {"master": master,
                   "person": person,
                   "orders": order_s,
                   'production': production,
                   'production_employee': production_employee,
                   }

        return render(request, 'users/master.html', context)