from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from basketapp.models import BasketItem
from mainapp.models import Product
from ordersapp.models import OrderItem


@login_required
def index(request):
    basket_items = BasketItem.objects.filter(user=request.user)
    context = {
        'page_title': 'корзина',
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse(
            'main:product_page',
            kwargs={'pk': pk}
        ))
    product = get_object_or_404(Product, pk=pk)
    basket = BasketItem.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(BasketItem, pk=pk).delete()
    return HttpResponseRedirect(reverse('basket:index'))


def change(request, pk, quantity):
    if request.is_ajax():
        basket_item = BasketItem.objects.filter(pk=pk).first()
        if quantity == 0:
            basket_item.delete()
        else:
            basket_item.quantity = quantity
            basket_item.save()

        context = {
            'basket_items': request.user.user_basket.all(),
        }
        basket_items = loader.render_to_string(
            'basketapp/includes/inc__basket_items.html', context=context, request=request
        )
        return JsonResponse({
            'basket_items': basket_items
        })


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
