from django.core.management.base import BaseCommand
from first_app.models import Order, OrderItem
from datetime import datetime, timedelta
from random import randint
datetime_start = datetime(2018, 1, 1, 9, 0, 0)

class Command(BaseCommand):
    help = 'Generate some orders with items'

    def add_arguments(self, parser):
        parser.add_argument('number_of_orders', type=int, help='Indicates the number of orders to be created')

    def handle(self, *args, **kwargs):
        number_of_orders = kwargs['number_of_orders']

        # Для определения номера итерации используется count (предполагается, что удаляться заказы не будут)
        # Как вариант можно использовать максимальный номер или же создать модель с номером итерации - наиболее точно
        count = Order.objects.all().count()
        for orders_number in range(number_of_orders):

            # Номер заказа
            number = count+orders_number+1

            # Создание и запись объекта заказа
            Order(number=number,
                  created_date=datetime_start+timedelta(hours=number-1)).save()

            for items_number in range(randint(1,5)):

                # Создание и запись элемента заказа
                OrderItem(order_id = number,
                          product_name='Товар-'+str(items_number+1),
                          product_price=randint(100,9999),
                          amount = randint(1,10)).save()








#class Command(BaseCommand):
#    help = 'Generate some orders with items'


    #def handle(self, *args, **kwargs):




      #  print('Заказы созданы '+str(number_of_orders))
