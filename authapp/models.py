from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopClient(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)

    def basket_cost(self):
        return sum(item.product.price * item.quantity for item in self.user_basket.all())

    def basket_total_quantity(self):
        return sum(item.quantity for item in self.user_basket.all())
