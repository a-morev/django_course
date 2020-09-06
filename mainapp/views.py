from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    categories = ProductCategory.objects.all()

    context = {
        'page_title': 'каталог',
        'categories': categories,
    }
    return render(request, 'mainapp/catalog.html', context)


def product_page(request, pk):
    context = {
        'page_title': 'товар',
        'categories': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product_page.html', context)


def category(request, pk):
    if pk == 0:
        item = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        item = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category=item)

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
