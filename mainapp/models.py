from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=128)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория продукта')
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=64, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.IntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @classmethod
    def get_items(cls):
        return cls.objects.filter(is_active=True)
