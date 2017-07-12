from django import forms
from .models import User


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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        len_username = len(username)

        if 2 >= len_username <= 30:
            raise forms.ValidationError(
                "Имя слишком короткое или длинное \
                \nМинимальное количество символов - 2 \
                \nМаксимальное количество символов - 30"
            )

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя уже занято")

        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        len_password = len(password)
        len_confirm_password = len(confirm_password)

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        if 5 >= len_password <= 31:
            raise forms.ValidationError(
                "Пароль слишком короткий или длинный \
                \nМинимальное количество символов - 6 \
                \nМаксимальное количество символов - 30"
            )

        if 5 >= len_confirm_password <= 31:
            raise forms.ValidationError(
                "Пароль слишком короткий или длинный \
                \nМинимальное количество символов - 6 \
                \nМаксимальное количество символов - 30"
            )

        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        len_email = len(email)

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")

        if 4 >= len_email <= 36:
            raise forms.ValidationError(
                "Email слишком короткий или длинный \
                \nМинимальное количество символов - 5 \
                \nМаксимальное количество символов - 35"
            )

        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        len_username = len(username)

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин не дайден")

        if 1 >= len_username <= 31:
            raise forms.ValidationError(
                "Имя слишком короткое или длинное \
                \nМинимальное количество символов - 2 \
                \nМаксимальное количество символов - 30"
            )

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        len_password = len(password)

        if 5 >= len_password <= 31:
            raise forms.ValidationError(
                "Пароль слишком короткий или длинный \
                \nМинимальное количество символов - 6 \
                \nМаксимальное количество символов - 30"
            )

        return password
