from django.contrib import admin

from .models import CalDAVAccount


class CalDAvAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'username', 'url'
    )


admin.site.register(CalDAVAccount, CalDAvAccountAdmin)
