from django.contrib import admin
from .models import RailroadAccount, RailroadStation


class RailroadAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'homeplace', 'workplace'
    )


admin.site.register(RailroadAccount, RailroadAccountAdmin)


class RailroadStationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(RailroadStation, RailroadStationAdmin)
