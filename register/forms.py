from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        labels = {
            "username": "Имя пользователя",
            "email": "Email адрес",
            "password": "Пароль",
        }
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        return super(RegisterForm, self).save(commit=commit)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        len_username = len(username)

        if 5 > len_username < 30:
            raise forms.ValidationError("Неправильное количество символов")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя занято")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        len_password = len(password)

        if 5 > len_password < 30:
            raise forms.ValidationError("Неправильное количество символов")

        return password

    def clean_confirm_password(self):
        user_password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        len_confirm_password = len(confirm_password)

        if 5 > len_confirm_password < 30:
            raise forms.ValidationError("Неправильное количество символов")

        if user_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        return user_password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        len_email = len(email)

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")

        if 4 > len_email < 30:
            raise forms.ValidationError("Неправильное количество символов")

        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        len_username = len(username)

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Такой логин не дайден")

        if 2 > len_username < 30:
            raise forms.ValidationError("Неправильное количество символов")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        len_password = len(password)

        if 5 > len_password < 30:
            raise forms.ValidationError("Неправильное количество символов")

        return password
