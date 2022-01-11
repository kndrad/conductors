from django.contrib import admin
from .models import Crew, Member


class TrainCrewAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'date'
    )


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'person', 'phone', 'profession', 'start_location', 'end_location'
    )


admin.site.register(Crew, TrainCrewAdmin)
admin.site.register(Member, MemberAdmin)
