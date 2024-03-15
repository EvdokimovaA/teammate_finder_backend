from django.contrib import admin
from .models import Users, Subscribers, Friends


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser',
                    'city', 'gender', 'birthday', 'who_search', 'photo', 'about_me', 'password')
    search_fields = ('username', 'id',)
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(Users, UsersAdmin)


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('user1_id', 'user2_id', 'is_subscribed1', 'is_subscribed2')
    search_fields = ('user1_id', 'user2_id',)


admin.site.register(Subscribers, SubscribersAdmin)


class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user1_id', 'user2_id')
    # readonly_fields = ('user1_id', 'user2_id')


admin.site.register(Friends, FriendsAdmin)
