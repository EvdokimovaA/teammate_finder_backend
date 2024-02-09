from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta, date


class Users(AbstractUser):
    GENDER_CHOICES = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
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


class Subscribers(models.Model):
    user1_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name='Пользователь',
                                 related_name='subscriber1')
    user2_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name='Подписчик',
                                 related_name='subscriber2')
    is_subscribed1 = models.BooleanField(verbose_name='Подписка user1', default=False)
    is_subscribed2 = models.BooleanField(verbose_name='Подписка user2', default=False)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Friends(models.Model):
    user_id = models.BigIntegerField(verbose_name='user_id')
    friend_id = models.BigIntegerField(verbose_name='friend_id')

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
