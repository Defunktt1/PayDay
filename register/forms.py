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
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя занято")
        return username

    def clean_confirm_password(self):
        user_password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if user_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return user_password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")
        return email
