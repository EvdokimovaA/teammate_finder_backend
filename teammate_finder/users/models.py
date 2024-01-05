from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta, date


class Users(AbstractUser):
    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    )
    city = models.CharField(max_length=100, verbose_name='Город')
    gender = models.CharField(choices=GENDER_CHOICES, verbose_name='Пол')
    birthday = models.DateField(auto_now=False, verbose_name='Дата рождения', null=True, blank=True, default=date.today)
    who_search = models.TextField(verbose_name='Кого ищу', null=True, blank=True)
    photo = models.ImageField(verbose_name='Фото', upload_to="photos/", null=True, blank=True)
    about_me = models.TextField(verbose_name='О себе', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
