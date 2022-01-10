from django.contrib import admin

from .models import RailroadAccount, RailroadStation, PublicTrain


class RailroadAccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'homeplace', 'workplace', 'administration_time'
    )


admin.site.register(RailroadAccount, RailroadAccountAdmin)


class RailroadStationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(RailroadStation, RailroadStationAdmin)


class PublicRailroadTrainAdmin(admin.ModelAdmin):
    list_display = (
        'trip', 'carrier',
        'departure_date', 'departure_station', 'departure_platform',
        'arrival_date', 'arrival_station', 'arrival_platform',
    )


admin.site.register(PublicTrain, PublicRailroadTrainAdmin)
