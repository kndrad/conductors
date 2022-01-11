from django.contrib import admin

from .models import Allocation, Action


class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'signature', 'start_date', 'end_date', 'last_updated',
    )


class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'trip', 'name', 'date', 'start_location', 'start_hour', 'end_location', 'end_hour'
    )


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Action, ActionAdmin)
