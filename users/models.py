
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


def email_validator(value: str):
    """Запрет регистрации с рамблера"""

    if value.endswith('@rambler.ru'):
        raise ValidationError("Недопустимый почтовый домен")



class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lat = models.FloatField(verbose_name="Широта", null=True, blank=True)
    lng = models.FloatField(verbose_name="Долгота", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    username = models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя(логин)")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    role = models.CharField(max_length=50, verbose_name="Роль")
    age = models.IntegerField(verbose_name="Возраст")  # нужно будет удалить, оставляю для соответствия старым фикстурам
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Локация")
    email = models.EmailField(unique=True, blank=True, validators=[email_validator], verbose_name="Почта")
    birth_date = models.DateField( verbose_name="Дата рождения")

    def __str__(self):
        return self.username

    @property
    def location_name(self):
        return self.location.name if self.location else None

    class Meta:
        ordering = ['first_name']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"
