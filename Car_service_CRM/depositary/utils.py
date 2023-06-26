from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import redirect

from depositary.forms import DepositaryForm, DepositaryOwnerForm
from depositary.models import Depositary
from service.forms import WorksForm
from users.models import Person
from service.models import Orders, WorksOrder


def master_access(func):
    def index(request, *args, **kwargs):
        # person = Person.objects.get(user=request.user)
        if Person.objects.get(user=request.user).jod_title == "Мастер":
            return func(request, *args, **kwargs)
        return redirect('order-for-mechanical')

    return index


def context_depositary(request, *args, **kwargs):
    person = Person.objects.get(user=request.user)
    form = DepositaryForm()
    return {'person': person, 'form': form, 'parts_style': 'none'}


def context_detail(request, pk, *args, **kwargs):
    person = Person.objects.get(user=request.user)
    detail = Depositary.objects.get(id=pk)
    return {'person': person, 'detail': detail, 'parts_style': 'none', 'owner__parts_style': 'none'}


def context_edit_detail(request, pk, *args, **kwargs):
    person = Person.objects.get(user=request.user)
    detail = Depositary.objects.get(id=pk)
    form = DepositaryForm(instance=detail)
    return {'person': person, 'detail': detail, 'form': form, 'parts_style': '',
            'owner__parts_style': 'none', 'btn_style': 'color:red; font-weight: 600'}


def context_owner_of_detail(request, pk, *args, **kwargs):
    person = Person.objects.get(user=request.user)
    detail = Depositary.objects.get(id=pk)
    form = DepositaryOwnerForm(instance=detail)
    return {'person': person, 'detail': detail, 'form_owner': form, 'owner__parts_style': '',
            'parts_style': 'none', 'btn1_style': 'color:red; font-weight: 600'}


def search_parts(search_query, start_date, end_date):
    if search_query and start_date and end_date:
        parts = Depositary.objects.filter(date_opening__gte=start_date) & \
                Depositary.objects.filter(date_opening__lt=end_date) & \
                Depositary.objects.filter(Q(part_name__iregex=search_query) |
                                          Q(part_number__iregex=search_query))

    elif search_query:
        parts = Depositary.objects.distinct().filter(Q(part_name__iregex=search_query) |
                                                     Q(part_number__iregex=search_query))

    elif start_date and end_date:
        parts = Depositary.objects.filter(date_opening__gte=start_date) & \
                Depositary.objects.filter(date_opening__lt=end_date)

    elif start_date:
        parts = Depositary.objects.filter(date_opening__gte=start_date)

    elif end_date:
        parts = Depositary.objects.filter(date_opening__lt=end_date)

    else:
        parts = Depositary.objects.filter(date_closing=None)
    return parts

