from django.shortcuts import render, redirect, HttpResponse
from .models import Orders, WorksOrder
from django.shortcuts import get_object_or_404
# форма авторизации пользователя
from django.contrib.auth.forms import AuthenticationForm
# вход в аккаунт; выход из аккаунта; авторизация
from django.contrib.auth import login, logout, authenticate
# декоратор для ограничения доступа незарегистрированным пользователям
from django.contrib.auth.decorators import login_required
from .forms import OrdersForm, WorksForm
from .models import Orders, WorksOrder
from django.db.models import Sum


# Главная страница с нарядами
@login_required
def index(request):
    if request.method == "GET":
        orders = Orders.objects.filter(date_completed__isnull=True)
        context = {'orders': orders, 'form__add_order': OrdersForm()}
        return render(request, 'service/index.html', context)
    if request.method == "POST":
        try:
            form = OrdersForm(request.POST)
            form.save()
            return redirect('index')
        except ValueError:
            context = {'form__add_order': OrdersForm(),
                       'error': 'Некорректный ввод данных, попробуйте еще раз'}
            return render(request, 'service/index.html', context)


# Закрытые наряды
@login_required
def closer_orders(request):
    orders = Orders.objects.filter(date_completed__isnull=False)
    context = {'orders': orders}
    return render(request, 'service/closed-orders.html', context)


# добавление работ под наряд
@login_required
def worksorder(request, pk):
    order = get_object_or_404(Orders, id=pk)
    works = WorksOrder.objects.filter(order=order)
    context = {'works': works, 'order': order, 'form': WorksForm()}
    if request.method == "GET":
        return render(request, 'service/worksorder.html', context)
    else:
        try:
            form = WorksForm(request.POST)
            new_form = form.save(commit=False)
            new_form.final_price = new_form.standard * new_form.price
            new_form.order = order
            new_form.save()
            # return render(request, 'service/worksorder.html', context)
            return redirect(request.META.get('HTTP_REFERER'))
        except ValueError:
            return render(request, 'service/worksorder.html', context)


# авторизация
def loginuser(request):
    if request.method == "GET":
        context = {'form': AuthenticationForm()}
        return render(request, 'service/loginuser.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'}
            return render(request, 'service/loginuser.html', context)
        else:
            login(request, user)
            return redirect('index')


# выход из акк
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')


# удаление работ из наряда
def delete_work(request, pk):
    if request.method == "GET":
        work = get_object_or_404(WorksOrder, id=pk)
        work.delete()
        # возврат обратно на страницу
        return redirect(request.META.get('HTTP_REFERER'))


# изменение статуса работы
def at_work(request, pk):
    # наряд к которому привязана работа
    work = WorksOrder.objects.get(id=pk).order
    if request.method == "GET":
        if WorksOrder.objects.filter(id=pk, order_status="Согласование"):
            WorksOrder.objects.filter(id=pk).update(order_status="В работе")
            # сумма стоимости работ под наряд
            order_sum = WorksOrder.objects.filter(order=work, order_status='В работе').aggregate(Sum("final_price"))
            work.final_price = order_sum['final_price__sum']
            work.save()
        else:
            WorksOrder.objects.filter(id=pk).update(order_status="Согласование")
            # сумма стоимости работ под наряд
            order_sum = WorksOrder.objects.filter(order=work, order_status='В работе').aggregate(Sum("final_price"))
            work.final_price = order_sum['final_price__sum']
            work.save()
        return redirect(request.META.get('HTTP_REFERER'))


# редактирование работы
def edit_work(request, pk):
    pass
#     works = WorksOrder.objects.filter(id=pk)
#     context = {'works': works, 'form': WorksForm()}
#     if request.method == "GET":
#         return render(request, 'service/worksorder.html', context)
