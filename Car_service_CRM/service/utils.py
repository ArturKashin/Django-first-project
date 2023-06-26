from django.core.paginator import Paginator
from django.db.models import Q
from service.models import Orders


def paginator_order(request, orders):
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return orders


def search_order(search_query, start_date, end_date, bull):
    if search_query and start_date and end_date:
        orders = Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__gte=start_date) & \
                 Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__lt=end_date) & \
                 Orders.objects.filter(Q(date_completed__isnull=bull),
                                       Q(vin_number__iregex=search_query) |
                                       Q(registration_number__iregex=search_query) |
                                       Q(client__iregex=search_query))

    elif search_query:
        orders = Orders.objects.filter(Q(date_completed__isnull=bull),
                                       Q(vin_number__iregex=search_query) |
                                       Q(registration_number__iregex=search_query) |
                                       Q(client__iregex=search_query))

    elif start_date and end_date:
        orders = Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__gte=start_date) & \
                 Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__lt=end_date)

    elif start_date:
        orders = Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__gte=start_date)

    elif end_date:
        orders = Orders.objects.filter(date_completed__isnull=bull,
                                       date_start__lt=end_date)

    else:
        orders = Orders.objects.filter(date_completed__isnull=bull)
    return orders


