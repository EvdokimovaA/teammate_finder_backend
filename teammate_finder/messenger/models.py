from django.db import models
from users.models import Users


class Chats(models.Model):
    user1_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name='Участник_1',
                                 related_name='chat_member1')
    user2_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name='Участник_2',
                                 related_name='chat_member2')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Messages(models.Model):
    MESSAGE_STATES = (
        ('Отправлено', 'Отправлено'),
        ('Получено', 'Получено'),
        ('Прочитано', 'Прочитано'),
    )

    chat_id = models.ForeignKey(Chats, on_delete=models.CASCADE, null=True, verbose_name='№_чата')
    sender_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name='id_отправителя')
    receiving_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Время_получения')
    message_status = models.CharField(choices=MESSAGE_STATES, verbose_name='Статус_сообщения')
    content = models.TextField(verbose_name='Содержание_сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['receiving_time']
