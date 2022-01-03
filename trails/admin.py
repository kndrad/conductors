from django.contrib import admin

from trails.models import Trail, TrailStation


class TrailAdmin(admin.ModelAdmin):
    list_display = ('user', 'beginning', 'finale', 'last_driven')


admin.site.register(Trail, TrailAdmin)


class TrailStationAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(TrailStation, TrailStationAdmin)
