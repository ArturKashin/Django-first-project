from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from service.models import Orders
from .utils import *
from .models import Depositary
from .forms import DepositaryForm


# склад, поиск
@login_required(login_url='loginuser')
@master_access
def depositary(request):
    if request.method == "GET":
        search_query = request.GET.get('search', '')
        start_date = request.GET.get('start-date', '')
        end_date = request.GET.get('end-date', '')
        parts = search_parts(search_query, start_date, end_date)

        paginator = Paginator(parts, 30)
        page_number = request.GET.get('page')
        parts = paginator.get_page(page_number)

        context = {**context_depositary(request), 'parts': parts}
        return render(request, 'depositary/depositary.html', context)


# добавление деталей
@login_required(login_url='loginuser')
@master_access
def add_part(request):
    if request.method == "POST":
        form = DepositaryForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.part_number = new_form.part_number.upper()
            new_form.part_name = new_form.part_name.lower()
            new_form.output_cost = (new_form.input_cost + (new_form.input_cost / 100 * new_form.markup_cost)) * new_form.quantity
            new_form.save()
            messages.success(request, f"Позиция '{new_form.part_name}' добавлена на склад")
            return redirect('depositary')


# просмотр отдельной детали
@login_required(login_url='loginuser')
@master_access
def detail(request, pk):
    context = context_detail(request, pk)
    return render(request, 'depositary/detail.html', context)


# изменение детали
@login_required(login_url='loginuser')
@master_access
def edit_detail(request, pk):
    current_detail = Depositary.objects.get(id=pk)
    if request.method == 'POST':
        form = DepositaryForm(request.POST, instance=current_detail)
        if form.is_valid():
            form_edit = form.save(commit=False)
            form_edit.output_cost = (form_edit.input_cost + (form_edit.input_cost / 100 * form_edit.markup_cost)) * form_edit.quantity
            form_edit.save()
            return redirect(f'/depositary/detail/{pk}/')
    context = context_edit_detail(request, pk)
    return render(request, 'depositary/detail.html', context)


# удаление(списание) со склада
@login_required(login_url='loginuser')
@master_access
def delete_detail(request, pk):
    current_detail = Depositary.objects.get(id=pk)
    if current_detail.order is None:
        current_detail.delete()
        messages.success(request, f"Деталь '{current_detail.part_name}' успешно удалена со склада")
        return redirect('depositary')
    else:
        messages.success(request, f"Деталь '{current_detail.part_name}' зарезервирована, удаление невозможно!")
        return redirect(f'/depositary/detail/{pk}/')


# закрепление детали за з/наряд
@login_required(login_url='loginuser')
@master_access
def owner_of_detail(request, pk):
    current_detail = Depositary.objects.get(id=pk)
    if request.method == "POST":
        form = DepositaryOwnerForm(request.POST, instance=current_detail)
        if form.is_valid():
            form.save()
            if current_detail.order:
                text = f'зарезервирована под {current_detail.order}'
            else:
                text = f'не зарезервирована'
            messages.success(request, f"Деталь '{current_detail.part_name}' {text}")
        return redirect(f'/depositary/detail/{pk}/')
    context = context_owner_of_detail(request, pk)
    return render(request, 'depositary/detail.html', context)


# удалить деталь из з/наряда
@login_required(login_url='loginuser')
@master_access
def remove_detail_from_order(request, pk):
    current_detail = Depositary.objects.get(id=pk)
    order = current_detail.order
    current_detail.order = None
    current_detail.save()
    return redirect(f'/worksorder/{order.id}/')


# добавление детали через з/наряд
@login_required(login_url='loginuser')
@master_access
def add_detail(request, pk, sk):
    order = Orders.objects.get(id=pk)
    current_detail = Depositary.objects.get(id=sk)
    current_detail.order = order
    current_detail.save()

    return redirect(f'/worksorder/{pk}/')


# открыть з/наряд через склад
@login_required(login_url='loginuser')
@master_access
def open_order(request, pk):
    order = Orders.objects.get(id=pk)
    if order.date_completed:
        return redirect(f'/closed-works/{pk}')
    else:
        return redirect(f'/worksorder/{pk}/')
