from django.shortcuts import render, HttpResponseRedirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.clean_username()
            user_email = form.clean_email()
            user_password = form.clean_confirm_password()
            user = User.objects.create_user(user_name, user_email, user_password)
            user.save()
            messages.success(request, "Регистрация прошла успешно!")
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Добро пожаловать, {0}".format(username))
                return HttpResponseRedirect("/")
    else:
        form = LoginForm()

    return render(request, 'register/login.html', {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "До свидания!")
    return HttpResponseRedirect("/")
