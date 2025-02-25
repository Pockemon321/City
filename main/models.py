from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

def validate_image_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Поддерживаются только изображения (jpg, jpeg, png, gif)')
    if value.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError('Размер файла не должен превышать 10MB')

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
        validators=[validate_image_file],
        verbose_name='Фото проблемы',
        null=True,
        blank=True
    )
    after_image = models.ImageField(
        upload_to='solved_images/',
        validators=[validate_image_file],
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
