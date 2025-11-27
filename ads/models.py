from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from users.models import User

class CreatedTimeModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    class Meta:
        abstract = True

class Ad(CreatedTimeModels):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(10)], verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Comment(CreatedTimeModels):
    text = models.TextField(verbose_name="Текс")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Обьявление")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"
