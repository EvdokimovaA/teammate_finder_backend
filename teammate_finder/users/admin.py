from django.contrib import admin
from .models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name',
                    'city', 'gender', 'birthday', 'who_search', 'photo', 'about_me')
    search_fields = ('username', 'id',)
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(Users, UsersAdmin)
