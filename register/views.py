from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user_name = form.clean_username()
                user_email = form.clean_email()
                user_password = form.clean_confirm_password()
                user = User.objects.create_user(user_name, user_email, user_password)
                user.save()

            except ValidationError as ve:
                messages.add_message(request, messages.ERROR, ve)

    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {"form": form})
