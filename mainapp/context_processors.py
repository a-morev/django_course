from mainapp.models import ProductCategory


def catalog_menu(request):
    return {'catalog_menu': ProductCategory.objects.filter(is_active=True)}
