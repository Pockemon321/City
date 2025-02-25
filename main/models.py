from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('solved', 'Решена'),
        ('rejected', 'Отклонена'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True)
    before_image = models.ImageField(
        upload_to='problem_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])],
        verbose_name='Фото проблемы',
        null=True,
        blank=True
    )
    after_image = models.ImageField(
        upload_to='solved_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])],
        null=True,
        blank=True,
        verbose_name='Фото решения'
    )
    rejection_reason = models.TextField(null=True, blank=True, verbose_name='Причина отказа')

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
