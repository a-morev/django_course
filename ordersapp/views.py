from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OnlyLoggedUserMixin:
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderList(OnlyLoggedUserMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(OnlyLoggedUserMixin, CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):  # формирование formset
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(  # формирование class OrderFormSet
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.user_basket.all()
            if basket_items and len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket_items)
                )
                formset = OrderFormSet()
                # zip()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
                    form.initial['price'] = basket_item.product.price
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):  # проверяет и сохраняет форму
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()  # появляется Объект заказа
            if orderitems.is_valid():
                orderitems.instance = self.object  # реализация связи ОtoМ
                orderitems.save()
            self.request.user.user_basket.all().delete()

        # удаление пустого заказа
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderUpdate(OnlyLoggedUserMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):  # формирование formset
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST, self.request.FILES,
                instance=self.object
            )
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        data['orderitems'] = formset
        return data

    def form_valid(self, form):  # проверяет и сохраняет форму
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаление пустого заказа
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderDetail(OnlyLoggedUserMixin, DetailView):
    model = Order


class OrderDelete(OnlyLoggedUserMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')


@login_required()
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:index'))
