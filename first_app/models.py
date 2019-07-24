# from django.db import models
#
# class Order(models.Model):
#     number = models.IntegerField('number')
#
# class OrderItem(models.Model):
#     order_id = models.IntegerField('order_id')

from django.db import models

class Order(models.Model):
    number          = models.IntegerField('номер итерации')
    created_date    = models.DateTimeField('дата и время создания')

class OrderItem(models.Model):
    order_id = models.IntegerField('номер заказа')
    product_name = models.TextField('название')
    product_price = models.IntegerField('цена')
    amount = models.IntegerField('количество')
