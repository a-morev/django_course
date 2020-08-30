from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopClient(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
