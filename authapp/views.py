from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopLoginForm, ShopRegistrationForm, ShopProfileForm


def login(request):
    if request.method == 'POST':
        form = ShopLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopLoginForm()

    context = {
        'page_title': 'аутентификация',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        user = ShopRegistrationForm(request.POST, request.FILES)
        if user.is_valid():
            user.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        user = ShopRegistrationForm()

    context = {
        'page_title': 'регистрация',
        'form': user,
    }
    return render(request, 'authapp/register.html', context)


def profile(request):
    if request.method == 'POST':
        user = ShopProfileForm(request.POST, request.FILES, instance=request.user)
        if user.is_valid():
            user.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        user = ShopProfileForm(instance=request.user)  # обязательно добавить при редактировании
    context = {
        'page_title': 'профиль',
        'form': user,
    }
    return render(request, 'authapp/profile.html', context)
