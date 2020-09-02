from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopClient
from django.conf import settings
import os
import json

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'), encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category) for category in categories]

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        if not ShopClient.objects.filter(username='django').exists():
            ShopClient.objects.create_superuser(username='django', email='', password='geekbrains')
