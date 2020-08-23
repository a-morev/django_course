from django.shortcuts import render


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    context = {
        'page_title': 'каталог',
    }
    return render(request, 'mainapp/catalog.html', context)


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
