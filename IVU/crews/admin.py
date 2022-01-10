from django.contrib import admin

class TrainCrewAdmin(admin.ModelAdmin):
    list_display = (
        'trip', 'date'
    )


class TrainCrewMemberAdmin(admin.ModelAdmin):
    list_display = (
        'person', 'phone', 'profession', 'start_location', 'end_location'
    )


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(AllocationTrain, AllocationTrainAdmin)
admin.site.register(AllocationSchedule, AllocationDetailAdmin)
admin.site.register(AllocationTimetable, AllocationTimetableAdmin)
admin.site.register(TripCrew, TrainCrewAdmin)
admin.site.register(CrewMember, TrainCrewMemberAdmin)
