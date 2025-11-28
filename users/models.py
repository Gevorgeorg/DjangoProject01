from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from .us_manager import UserManager


def email_validator(value: str):
    if value.endswith('@rambler.ru'):
        raise ValidationError("Недопустимый почтовый домен")


class UserRoleChoices(models.TextChoices):
    admin = 'admin', "Админ"
    user = 'user', "Пользователь"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта", validators=[email_validator])
    password = models.CharField(max_length=128, verbose_name="Пароль")
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, default="", verbose_name="Фамилия")
    phone = PhoneNumberField(verbose_name="Телефон", region='RU')
    role = models.CharField(max_length=50, choices=UserRoleChoices.choices, default='user', verbose_name="Роль")
    is_staff = models.BooleanField(default=False, verbose_name="Служебный")
    is_superuser = models.BooleanField(default=False, verbose_name="Супер пользователь")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['first_name']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
