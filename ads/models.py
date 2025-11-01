from django.db import models


class Category(models.Model):
    name: str = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ads(models.Model):
    name: str = models.CharField(max_length=100, verbose_name="Заголовок")
    author: str = models.CharField(max_length=100, verbose_name="Автор")
    price: int = models.IntegerField(verbose_name="Цена")
    description: str = models.TextField(max_length=1200, verbose_name="Описание", blank=True)
    address: str = models.TextField(max_length=100, verbose_name="Адрес")
    is_published: bool = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return self.name
