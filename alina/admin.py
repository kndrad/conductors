from django.contrib import admin

from alina.models import Allocation, AllocationDetail, AllocationTimetable, TrainCrew, TrainCrewMember


class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_date', 'end_date', 'last_updated',
    )


class AllocationDetailAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'action', 'action_date', 'start_location', 'start_hour', 'end_location', 'end_hour'
    )


class AllocationTimetableAdmin(admin.ModelAdmin):
    list_display = (
        'month', 'year', 'user', 'last_updated',
    )


class TrainCrewAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'date'
    )


class TrainCrewMemberAdmin(admin.ModelAdmin):
    list_display = (
        'person', 'phone_number', 'profession', 'start_location', 'end_location'
    )


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(AllocationDetail, AllocationDetailAdmin)
admin.site.register(AllocationTimetable, AllocationTimetableAdmin)
admin.site.register(TrainCrew, TrainCrewAdmin)
admin.site.register(TrainCrewMember, TrainCrewMemberAdmin)
