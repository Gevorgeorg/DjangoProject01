from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Картинка")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "Обьявление"
        verbose_name_plural = "Обьявления"


class Selection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    items = models.ManyToManyField('Ad', verbose_name="Объявления в подборке")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
