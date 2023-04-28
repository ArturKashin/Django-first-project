from django.shortcuts import render, redirect, get_object_or_404
# декоратор для ограничения доступа незарегистрированным пользователям
from django.contrib.auth.decorators import login_required
from .forms import OrdersForm, WorksForm
from .models import Orders, WorksOrder
from django.db.models import Q
from users.models import Person
from django.contrib import messages
from datetime import datetime
from rest_framework import viewsets, permissions
from .serializers import OrderSerializer, WorksOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorksOrderViewSet(viewsets.ModelViewSet):
    queryset = WorksOrder.objects.all()
    serializer_class = WorksOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


# Главная страница с нарядами
@login_required
def index(request):
    if request.method == "GET":
        search_query = request.GET.get('search', '')
        person = Person.objects.get(user=request.user)
        if search_query:
            orders = Orders.objects.distinct().filter(Q(date_completed__isnull=True),
                                           Q(vin_number__icontains=search_query) |
                                           Q(registration_number__icontains=search_query))
        else:
            orders = Orders.objects.filter(date_completed__isnull=True)

        context = {'orders': orders, 'person': person, 'form': OrdersForm()}
        return render(request, 'service/index.html', context)
    if request.method == "POST":
        try:
            form = OrdersForm(request.POST)
            form.save()
            return redirect('index')
        except ValueError:
            context = {'form': OrdersForm(),
                       'error': 'Некорректный ввод данных, попробуйте еще раз',}
            return render(request, 'service/index.html', context)


# Открытые наряды для механиков
def order_for_mechanical(request):
    if request.method == "GET":
        search_query = request.GET.get('search', '')
        person = Person.objects.get(user=request.user)
        if search_query:
            orders = Orders.objects.filter(Q(date_completed__isnull=True),
                                           Q(vin_number__icontains=search_query) |
                                           Q(registration_number__icontains=search_query))
        else:
            orders = Orders.objects.filter(date_completed__isnull=True)

        context = {'orders': orders, 'person': person}
        return render(request, 'service/order-for-mechanical.html', context)


# работы для механика
def works_for_mechanical(request, pk):
    person = Person.objects.get(user=request.user)
    works = WorksOrder.objects.filter(order=pk)
    context = {'works': works, 'person': person}
    return render(request, 'service/works-for-mechanical.html', context)


# Закрытые наряды
@login_required
def closer_orders(request):
    person = Person.objects.get(user=request.user)
    search_query = request.GET.get('search', '')
    if search_query:
        orders = Orders.objects.filter(Q(date_completed__isnull=False),
                                       Q(vin_number__icontains=search_query) |
                                       Q(registration_number__icontains=search_query))
    else:
        orders = Orders.objects.filter(date_completed__isnull=False)
    context = {'orders': orders, 'person': person}
    return render(request, 'service/closed-orders.html', context)


# Закрытые работы
def closed_works(request, pk):
    person = Person.objects.get(user=request.user)
    order = Orders.objects.get(id=pk)
    works = WorksOrder.objects.filter(order=pk)
    context = {'works': works, 'person': person, 'order': order}
    return render(request, 'service/closed-works.html', context)


# добавление работ под наряд
@login_required
def worksorder(request, pk):
    order = Orders.objects.get(id=pk)
    works = WorksOrder.objects.filter(order=order)
    person = Person.objects.get(user=request.user)
    context = {'works': works, 'order': order, 'person': person, 'form': WorksForm()}
    if request.method == "GET":
        return render(request, 'service/worksorder.html', context)
    else:
        try:
            form = WorksForm(request.POST)
            new_form = form.save(commit=False)
            # стоимость работы
            new_form.final_price = new_form.standard * new_form.price
            new_form.order = order
            new_form.name = new_form.name.title()
            new_form.save()
            # подсчет стоимости наряда
            order.final_price += new_form.final_price
            order.save()
            return redirect(request.META.get('HTTP_REFERER'))
        except ValueError:
            return render(request, 'service/worksorder.html', context)


# удаление работ из наряда
def delete_work(request, pk):
    if request.method == "GET":
        work = get_object_or_404(WorksOrder, id=pk)
        # удаление стоимости работы из общей стоимости наряда
        order = work.order
        order.final_price -= work.final_price
        order.save()
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
        else:
            WorksOrder.objects.filter(id=pk).update(order_status="Согласование")

        return redirect(request.META.get('HTTP_REFERER'))


# завершение выполнения работы сотрудником
def executor_completed(request, pk):
    person = Person.objects.get(user=request.user)
    work = WorksOrder.objects.get(id=pk)
    work.executor = request.user
    work.order_status = 'Выполнено'
    person.time += work.standard
    person.save()
    work.save()
    return redirect(request.META.get('HTTP_REFERER'))


# редактирование работы(Продумать redirect/render после выхода из метода POST)
def edit_work(request, pk):
    person = Person.objects.get(user=request.user)
    work = WorksOrder.objects.get(id=pk)
    form = WorksForm(instance=work)

    works = WorksOrder.objects.filter(order=work.order)
    order = Orders.objects.get(id=work.order.id)
    context = {'form': form, 'works': works, 'person': person, 'order': order}

    if request.method == "POST":
        form = WorksForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'service/worksorder.html', context)


# закрытие наряда
def close_order(request, pk):
    person = Person.objects.get(user=request.user)
    order = Orders.objects.get(id=pk)
    works = WorksOrder.objects.filter(order=order)
    for work in works:
        if work.order_status != 'Выполнено':
            context = {'order': order, 'works': works, 'person': person}
            messages.error(request, 'Присутствуют не выполненные работы, удалите либо выполните работы!')
            return render(request, 'service/worksorder.html', context)
        else:
            order.date_completed = datetime.now()
            order.save()
            messages.success(request, "Наряд успешно закрыт")
            return redirect('index')


# Удаление наряда
def delete_order(request, pk):
    person = Person.objects.get(user=request.user)
    order = Orders.objects.get(id=pk)
    works = WorksOrder.objects.filter(order=order)
    context = {'order': order, 'works': works, 'person': person}
    for work in works:
        if work.order_status != 'Согласование':
            messages.error(request, 'Для удаления заказ наряда, переведите работы в статус согласования')
            return render(request, 'service/worksorder.html', context)
        else:
            order.delete()
            messages.success(request, 'Заказ наряд успешно удален')
            return redirect('index')