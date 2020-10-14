from mainapp.models import ProductCategory
from shop import settings
from django.core.cache import cache


def catalog_menu(request):
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
    else:
        links_menu = ProductCategory.objects.filter(is_active=True)

    return {'catalog_menu': links_menu}
