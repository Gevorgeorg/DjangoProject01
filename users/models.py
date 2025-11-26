from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def email_validator(value: str):
    if value.endswith('@rambler.ru'):
        raise ValidationError("Недопустимый почтовый домен")


class UserManager(BaseUserManager): # в отдельный фалй!!! это не модель а менеджер!! не место в models.py
    def create_user(self, email, first_name, last_name, phone, password=None): # TypeHints????
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None): # TypeHints????
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role="admin"
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта", validators=[email_validator])
    password = models.CharField(max_length=128, verbose_name="Пароль")
    last_login = models.DateTimeField(_('last login'), blank=True, null=True) # Слишком сложна
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия") # в админке не сохранится такое создание
    phone = models.CharField(max_length=15, verbose_name="Телефон") # PhoneNumberField есть езе для такого
    role = models.CharField(max_length=50, default='user', verbose_name="Роль") # где Choices почему свободное поле ввода если ты и так знаешь какие роли могут быть!
    is_staff = models.BooleanField(default=False) # ?    verbose_name???
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['first_name']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
