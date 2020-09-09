"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import adminapp.views as adminapp

# обязательно добавить
app_name = 'adminapp'

urlpatterns = [
    # path('', adminapp.index, name='index'),
    path('', adminapp.UserList.as_view(), name='index'),
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/<int:pk>/update/', adminapp.user_update, name='user_update'),
    path('user/<int:pk>/delete/', adminapp.user_delete, name='user_delete'),

    # path('categories/read/', adminapp.categories_read, name='categories_read'),
    path('categories/read/', adminapp.ProductCategoriesRead.as_view(), name='categories_read'),
    path('category/create/', adminapp.ProductCategoryCreate.as_view(), name='category_create'),
    path('category/<int:category_pk>/update/', adminapp.ProductCategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),

    path('category/<int:category_pk>/products/', adminapp.category_products, name='category_products'),
    path('category/<int:category_pk>/product/create/', adminapp.product_create, name='product_create'),
    path('product/<int:product_pk>/read/', adminapp.ProductDetail.as_view(), name='product_read'),
    path('product/<int:pk>/update/', adminapp.product_update, name='product_update'),
    path('product/<int:pk>/delete/', adminapp.product_delete, name='product_delete'),
]
