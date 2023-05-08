from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.models import Person
from .utils import master_access


@login_required
@master_access
def depositary(request):
    person = Person.objects.get(user=request.user)
    context = {'person': person}
    return render(request, 'depositary/depositary.html', context)
