from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserRegisterForm, AdminShopUserUpdateForm, AdminProductCategoryCreateForm, \
    AdminProductUpdateForm
from mainapp.models import ProductCategory, Product


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = get_user_model().objects.all().order_by(
#         '-is_active', '-is_superuser', '-is_staff', 'username'
#     )
#     context = {
#         'page_title': 'админка/пользователи',
#         'users_list': users_list,
#     }
#     return render(request, 'adminapp/shopclient_list.html', context)


# доступ только для админа
class OnlySuperUserMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# отображение заголовка страницы
class PageTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        if hasattr(self, 'page_title'):
            data['page_title'] = self.page_title
        return data


class UserList(OnlySuperUserMixin, PageTitleMixin, ListView):
    model = get_user_model()
    page_title = 'админка/пользователи'


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserRegisterForm()

    context = {
        'page_title': 'пользователи/создание',
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'page_title': 'пользователи/редактирование',
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'page_title': 'пользователи/удаление',
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def categories_read(request):
#     context = {
#         'page_title': 'админка/категории',
#         'categories_list': ProductCategory.objects.all(),
#     }
#     return render(request, 'adminapp/productcategory_list.html', context)


class ProductCategoriesRead(OnlySuperUserMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'
    # paginate_by = 2


class ProductCategoryCreate(OnlySuperUserMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    page_title = 'админка/категории/создание'
    success_url = reverse_lazy('my_admin:categories_read')
    # fields = '__all__'
    form_class = AdminProductCategoryCreateForm  # для отображения стилей в форме


class ProductCategoryUpdate(OnlySuperUserMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    page_title = 'админка/категории/редактирование'
    success_url = reverse_lazy('my_admin:categories_read')
    form_class = AdminProductCategoryCreateForm  # для отображения стилей в форме
    pk_url_kwarg = 'category_pk'

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                # self.object.product_set.update(price=5000)
                # self.object.product_set.update(is_active=False)
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                # db_profile_by_type(self.model, 'UPDATE', connection.queries)

        return super().form_valid(form)


class ProductCategoryDelete(OnlySuperUserMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    page_title = 'админка/категории/удаление'
    success_url = reverse_lazy('my_admin:categories_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def category_products(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    object_list = category.product_set.all()
    context = {
        'page_title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'adminapp/category_products_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'category_pk': category.pk}
            ))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
            }
        )

    context = {
        'page_title': 'продукты/создание',
        'form': form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'category_pk': product.category.pk}
            ))
    else:
        form = AdminProductUpdateForm(instance=product)

    context = {
        'page_title': 'продукты/редактирование',
        'form': form,
        'category': product.category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse(
            'my_admin:category_products',
            kwargs={'category_pk': obj.category.pk}
        ))

    context = {
        'page_title': 'продукты/удаление',
        'object': obj,
    }
    return render(request, 'adminapp/product_delete.html', context)


class ProductDetail(OnlySuperUserMixin, DetailView):
    model = Product
    pk_url_kwarg = 'product_pk'
