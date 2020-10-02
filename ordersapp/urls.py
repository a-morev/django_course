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
import ordersapp.views as ordersapp

# обязательно добавить
app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='order_update'),
    path('read/<int:pk>/', ordersapp.OrderDetail.as_view(), name='order_read'),
    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('forming/complete/<int:pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
]
