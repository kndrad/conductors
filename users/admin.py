from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'date_joined')


admin.site.register(User, UserAdmin)