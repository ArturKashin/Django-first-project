from django.shortcuts import redirect
from users.models import Person


def master_access(func):
    def index(request, *args, **kwargs):
        # person = Person.objects.get(user=request.user)
        if Person.objects.get(user=request.user).jod_title == "Мастер":
            return func(request, *args, **kwargs)
        return redirect('order-for-mechanical')

    return index
