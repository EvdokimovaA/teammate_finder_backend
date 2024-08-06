from django.contrib import admin
from .models import Chats, Messages


class ChatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1_id', 'user2_id')
    search_fields = ('id',)
    # readonly_fields = ('date_joined', 'last_login')


admin.site.register(Chats, ChatsAdmin)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'sender_id', 'receiving_time', 'content')
    # search_fields = ('id',)
    # readonly_fields = ('date_joined', 'last_login')


admin.site.register(Messages, MessagesAdmin)
