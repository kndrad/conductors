from django.contrib import admin
from .models import Crew, Member


class CrewAdmin(admin.ModelAdmin):
    list_display = (
        'trip', 'date'
    )


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'person', 'phone', 'profession', 'start_location', 'end_location'
    )


admin.site.register(Crew, CrewAdmin)
admin.site.register(Member, MemberAdmin)
