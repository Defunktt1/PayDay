from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    user_name = forms.CharField(label="Имя пользователя", min_length=2, max_length=50)
    user_email = forms.EmailField(label="Email")
    user_password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    confirm_user_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("user_name")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя занято")
        return username

    def clean_password(self):
        user_password = self.cleaned_data.get("user_password")
        confirm_user_password = self.cleaned_data.get("confirm_user_password")
        if user_password != confirm_user_password:
            raise forms.ValidationError("Пароли не совпадают")
        return user_password

    def clean_email(self):
        email = self.cleaned_data.get("user_email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")
        return email
