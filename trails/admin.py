from django.contrib import admin

from trails.models import Trail, StationAtTrail


class TrailAdmin(admin.ModelAdmin):
    list_display = ('user', 'beginning', 'finale', 'last_driven')


admin.site.register(Trail, TrailAdmin)


class StationAtTrailAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(StationAtTrail, StationAtTrailAdmin)
