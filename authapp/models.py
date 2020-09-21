

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from shop import settings
from shop.settings import USER_EXPIRES_TIMEDELTA


def get_activation_key_expires():
    return now() + USER_EXPIRES_TIMEDELTA


class ShopClient(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def basket_cost(self):
        return sum(item.product.price * item.quantity for item in self.user_basket.all())

    def basket_total_quantity(self):
        return sum(item.quantity for item in self.user_basket.all())

    def send_verify_mail(self):
        verify_link = reverse('auth:verify', kwargs={
            'email': self.email,
            'activation_key': self.activation_key,
        })

        title = f'Подтверждение учетной записи {self.username}'

        message = f'Для подтверждения учетной записи {self.username} на портале' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return self.email_user(
            title, message, settings.EMAIL_HOST_USER, fail_silently=False)

    class Meta:
        ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
