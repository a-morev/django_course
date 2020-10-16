from datetime import timedelta

from django.core.management.base import BaseCommand
# from django.db import connection
from django.db.models import F, Q, When, Case, IntegerField, DecimalField

# from basketapp.views import db_profile_by_type
from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='офис') | Q(category__name='модерн')
        # ).select_related('category')
        #
        # print(len(test_products))
        #
        # db_profile_by_type('learn db', '', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__cond = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__cond = Q(order__updated__gt=F('order__created') + action_1__time_delta) & Q(
            order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__cond = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__cond, then=ACTION_1)
        action_2__order = When(action_2__cond, then=ACTION_2)
        action_expired__order = When(action_expired__cond, then=ACTION_EXPIRED)

        action_1__profit = When(action_1__cond,
                                then=F('product__price') * F('quantity') * action_1__discount)

        action_2__profit = When(action_2__cond,
                                then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__profit = When(action_expired__cond,
                                      then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_profit=Case(
                action_1__profit,
                action_2__profit,
                action_expired__profit,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_profit').select_related('product')

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}: {orderitem.product.name:15}: '
                  f'скидка {abs(orderitem.total_profit):6.2f} руб. | '
                  f'{orderitem.order.updated - orderitem.order.created}')
