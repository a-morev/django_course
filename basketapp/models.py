from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete()


class BasketItem(models.Model):
    # objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(using=None, keep_parents=False)

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()
