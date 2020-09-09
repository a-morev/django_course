from random import choice

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_hot_product():
    products = Product.objects.all()
    return choice(products)


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    categories = ProductCategory.objects.all()
    hot_product = get_hot_product()

    context = {
        'page_title': 'каталог',
        'categories': categories,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/catalog.html', context)


def product_page(request, pk):
    context = {
        'page_title': 'товар',
        'categories': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product_page.html', context)


def category(request, pk, page=1):
    if pk == 0:
        item = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        item = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category=item)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'каталог',
        'categories': ProductCategory.objects.all(),
        'item': item,
        'products': products,
    }
    return render(request, 'mainapp/category.html', context)


def contacts(request):
    locations = [
        {
            'city': 'г. Томск',
            'phone': '+7 (3822) 88-88-88',
            'email': 'info_tom@domkol.ru',
            'address': 'ул. Лыткина, д.3А',
        },
        {
            'city': 'г. Новосибирск',
            'phone': '+7 (383) 888-88-88',
            'email': 'info_nsk@domkol.ru',
            'address': 'ул. Ленина, д.4А',
        }
    ]
    context = {
        'page_title': 'контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contacts.html', context)
