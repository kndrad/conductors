from django.contrib import admin

from IVU.timetables.models import Timetable


class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        'month', 'year', 'user', 'last_updated',
    )


admin.site.register(Timetable, TimetableAdmin)
