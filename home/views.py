from django.shortcuts import redirect, HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth import (
    login as auth_login, authenticate,
)
from .forms import LAuthenticationForm
from django.contrib import messages


def home(request):
    template_name = 'home/home.html'
    from schol_library.models import NumberBooks


    form = LAuthenticationForm()
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if Token.objects.filter(user_id=user.id).count() == 0:
                token = Token.objects.create(user=user)
                token.save_base()
                return redirect('account:dashboard')
            else:
                return redirect('account:dashboard')
        else:
            messages.error(request, 'Вы не правильно ввели логин или пароль. Повторите еще раз!')
            return render(request, template_name, {'form': form})
    else:
        return render(request, template_name, {'form': form})


def tech_view(request):
    return HttpResponse('Сайт на реконструкции до 10.04.2019 23:30')
