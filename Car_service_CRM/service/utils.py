from django.core.paginator import Paginator
from django.db.models import Q
from service.models import Orders, WorksOrder
import aspose.words as aw
import os


def paginator_order(request, orders):
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    orders_s = paginator.get_page(page_number)
    return orders_s


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


# печать з/наряда
def order_print(request, order):
    works = WorksOrder.objects.filter(order=order)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    # start table
    table = builder.start_table()

    # insert cell
    builder.insert_cell()
    table.auto_fit(aw.tables.AutoFitBehavior.AUTO_FIT_TO_CONTENTS)

    # set formatting and add text
    builder.cell_format.vertical_alignment = aw.tables.CellVerticalAlignment.CENTER
    builder.write("Номер")

    # insert cell
    builder.insert_cell()
    builder.write("Наименование")
    builder.insert_cell()
    builder.write("Стоимость")

    # end row
    builder.end_row()

    # insert another cell in the next row
    builder.insert_cell()

    # format cell and add text
    for i in range(1, len(works) + 1):
        builder.writeln(str(i))

    # insert another cell, set formatting and add text
    builder.insert_cell()
    for i in works:
        builder.writeln(f'{i.name}')

    builder.insert_cell()
    for i in works:
        builder.writeln(f'{i.final_price}')

    # end row
    builder.end_row()

    # insert another cell in the next row
    builder.insert_cell()
    builder.cell_format.horizontal_merge = aw.tables.CellMerge.FIRST
    builder.write("Итог:")

    builder.insert_cell()
    builder.cell_format.horizontal_merge = aw.tables.CellMerge.PREVIOUS

    builder.insert_cell()
    builder.cell_format.horizontal_merge = aw.tables.CellMerge.NONE
    total = 0
    for i in works:
        total += i.final_price
    builder.write(f'{total}')

    builder.end_row()

    table_style = doc.styles.add(aw.StyleType.TABLE, "MyTableStyle1").as_table_style()
    table_style.borders.line_width = 1
    table_style.left_padding = 18
    table_style.right_padding = 18
    table_style.top_padding = 12
    table_style.bottom_padding = 12

    table.style = table_style

    table.alignment = aw.tables.TableAlignment.CENTER

    # save document
    name_file = str(order.id) + '_' + str(order.client)
    doc.save(f"document_print/{name_file}.docx")
    os.startfile(f"C:\\Car service CRM\\Car_service_CRM\\document_print\\{name_file}.docx")
