from django.contrib.auth.models import AbstractUser
from django.db import models


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
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    username = models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя(логин)")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    role = models.CharField(max_length=100, verbose_name="Роль")
    age = models.IntegerField(verbose_name="Возраст")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def location_name(self):
        return self.location.name if self.location else None

    class Meta:
        ordering = ['first_name']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"
