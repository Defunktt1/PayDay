from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.
class User(models.Model):
    username = models.CharField('Имя пользователя', max_length=30, validators=[MinLengthValidator(2)])
    email = models.EmailField('Email', max_length=35, validators=[MinLengthValidator(5)])
    password = models.CharField('Пароль', max_length=30, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.username
