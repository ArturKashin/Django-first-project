from django.db.models import Q

from service.models import Orders


def search_worker_order(order, search_query, start_date, end_date):
    if search_query:
        orders = Orders.objects.filter(
            Q(id__in=order),
            Q(client__iregex=search_query) |
            Q(id__iregex=search_query) |
            Q(vin_number__iregex=search_query) |
            Q(registration_number__iregex=search_query)
        )
    # сортировка по дате
    elif start_date and end_date:
        orders = Orders.objects.filter(id__in=order,
                                       date_start__gte=start_date) & \
                 Orders.objects.filter(
                     id__in=order,
                     date_start__lt=end_date)

    elif start_date:
        orders = Orders.objects.filter(id__in=order,
                                       date_start__gte=start_date)

    elif end_date:
        orders = Orders.objects.filter(id__in=order,
                                       date_start__lt=end_date)

    else:
        orders = Orders.objects.filter(id__in=order)
    return orders
