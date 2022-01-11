from django.contrib import admin

from .models import RailroadAccount, VerifiedStation, Train


class RailroadAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'homeplace', 'workplace', 'administration_time'
    )


admin.site.register(RailroadAccount, RailroadAccountAdmin)


class VerifiedStationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(VerifiedStation, VerifiedStationAdmin)


class TrainAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'carrier',
        'departure_date', 'departure_station', 'departure_platform',
        'arrival_date', 'arrival_station', 'arrival_platform',
    )


admin.site.register(Train, TrainAdmin)
