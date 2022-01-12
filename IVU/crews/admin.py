from django.contrib import admin
from .models import TrainCrew, TrainCrewMember


class TrainCrewAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'date'
    )


class TrainCrewMemberAdmin(admin.ModelAdmin):
    list_display = (
        'person', 'phone', 'profession', 'start_location', 'end_location'
    )


admin.site.register(TrainCrew, TrainCrewAdmin)
admin.site.register(TrainCrewMember, TrainCrewMemberAdmin)
