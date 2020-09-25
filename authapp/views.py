from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopLoginForm, ShopRegistrationForm, ShopProfileForm
from authapp.models import ShopClient


def login(request):
    redirect_url = request.GET.get('next', None)

    if request.method == 'POST':
        form = ShopLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                redirect_url = request.POST.get('redirect_url', None)
                auth.login(request, user)
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopLoginForm()

    context = {
        'page_title': 'аутентификация',
        'form': form,
        'redirect_url': redirect_url,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.send_verify_mail():
                print('На Вашу почту отправлено сообщение подтверждения аккаунта')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopRegistrationForm()

    context = {
        'page_title': 'регистрация',
        'form': form,
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


def verify(request, email, activation_key):
    try:
        user = ShopClient.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'Ошибка активации пользователя: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'Ошибка активации пользователя: {err.args}')
        return HttpResponseRedirect(reverse('main'))
