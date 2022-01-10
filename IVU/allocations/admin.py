from django.contrib import admin

from .models import Timetable, Allocation, Action


class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        'month', 'year', 'user', 'last_updated',
    )


class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'signature', 'start_date', 'end_date', 'last_updated',
    )


class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'name', 'date', 'start_location', 'start_hour', 'end_location', 'end_hour'
    )


admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Action, ActionAdmin)
