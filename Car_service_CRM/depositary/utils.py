from django.shortcuts import redirect

from depositary.forms import DepositaryForm, DepositaryOwnerForm
from depositary.models import Depositary
from users.models import Person
from service.models import Orders


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


def context_add_detail(request, pk, sk, *args, **kwargs):
    order = Orders.objects.get(id=pk)
    detail = Depositary.objects.get(id=sk)
    detail.order = order
    detail.save()
    print(order, detail)