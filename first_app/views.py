from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, OrderItem
from django.db import connection
from django.db.models import Sum
import operator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import Min, Max

@csrf_exempt
def period(request):

    if 'from' not in request.POST:
        date1 = Order.objects.aggregate(Min('created_date'))['created_date__min']
    else:
        date1 = datetime.strptime(request.POST['from'], "%Y-%m-%d %H:%M:%S")


    if 'to' not in request.POST:
        date2 = Order.objects.aggregate(Max('created_date'))['created_date__max']
    else:
        date2 = datetime.strptime(request.POST['to'], "%Y-%m-%d %H:%M:%S")


    orders = Order.objects.all().filter(created_date__gte=date1, created_date__lte=date2).order_by('created_date')
    result = []
    for order in orders:
        local={}
        local['created_date']=order.created_date
        local['number']=order.number
        orderItems = OrderItem.objects.filter(order_id=order.number)
        articles = ''
        sum = 0
        for orderItem in orderItems:
            articles += orderItem.product_name+'*'+str(orderItem.amount)+' '
            sum += orderItem.product_price*orderItem.amount
        local['articles'] = articles
        local['sum'] = sum
        result.append(local)
    queries = connection.queries
    dates_1 = Order.objects.values_list('created_date', flat=True)
    dates=[]
    for date in dates_1:
        dates.append(str(date)[:-6])
    context = {'orders': result, 'queries' : queries, 'dates':dates, 'date1':date1, 'date2':date2}
    return render(request, 'first_app/period.html', context)


def top100(request):

    orders = {}

    # Получение всех названий товаров
    items = OrderItem.objects.values_list('product_name', flat=True)

    # Исключение повторяющихся
    items = list(set(items))

    # Подсчет количества товаров
    for item in items:
        orders[item] = OrderItem.objects.filter(product_name=item).aggregate(Sum('amount'))['amount__sum']

    # Сортировка товаров по убыванию
    sorted_orders = sorted(orders.items(), key=operator.itemgetter(1), reverse=True)

    # Инициализация результирующего словаря
    result = []

    # Обход всех товаров по порядку
    for sorted_order in sorted_orders:

        # Инициализация словаря для одного товара
        local = {}

        # Запись названия товара в словарь товара
        local['product_name'] = sorted_order[0]

        # Определение всех номеров заказов по данному товару
        id_list = list(OrderItem.objects.filter(product_name=local['product_name']).values_list('order_id', flat=True))
        local_orders = Order.objects.filter(number__in=id_list)

        local['data'] = ''
        for local_order in local_orders:
            local_item = OrderItem.objects.get(order_id=local_order.number, product_name=item)
            local['data'] += f'Заказ {local_order.number} - Цена {local_item.product_price} - Дата {local_order.created_date}, '

        result.append(local)

    queries = connection.queries
    context = {'orders': result, 'queries' : queries}
    return render(request, 'first_app/top100.html', context)


