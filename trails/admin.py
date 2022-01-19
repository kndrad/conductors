from django.contrib import admin

from trails.models import Trail, Waypoint


class TrailAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'last_driven')


admin.site.register(Trail, TrailAdmin)


class WaypointAdmin(admin.ModelAdmin):
    list_display = ('name', 'trail')


admin.site.register(Waypoint, WaypointAdmin)
