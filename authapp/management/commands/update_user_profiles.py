from django.core.management.base import BaseCommand
from authapp.models import ShopClient, ShopClientProfile


class Command(BaseCommand):
    help = 'Create user profile'

    def handle(self, *args, **options):
        # print(ShopClient.objects.filter(shopclientprofile__isnull=True).count())
        for user in ShopClient.objects.filter(shopclientprofile__isnull=True):
            ShopClientProfile.objects.create(user=user)
            # user.shopclientprofile = ShopClientProfile.objects.create(user=user)
            # user.save()
