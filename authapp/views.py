from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopLoginForm


def login(request):
    form = None
    if request.method == 'POST':
        form = ShopLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    elif request.method == 'GET':
        form = ShopLoginForm()

    context = {
        'page_title': 'аутентификация',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    pass


def register(request):
    pass
