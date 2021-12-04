from django.contrib import admin
from .models import RailroadAccount, RailroadStation, PublicRailroadTrain


class RailroadAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'homeplace', 'workplace', 'spare_time'
    )


admin.site.register(RailroadAccount, RailroadAccountAdmin)


class RailroadStationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(RailroadStation, RailroadStationAdmin)


class PublicRailroadTrainAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'carrier',
        'departure_date', 'departure_station', 'departure_platform',
        'arrival_date', 'arrival_station', 'arrival_platform',
    )


admin.site.register(PublicRailroadTrain, PublicRailroadTrainAdmin)
