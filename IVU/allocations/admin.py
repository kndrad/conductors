from django.contrib import admin

from .models import Allocation, AllocationAction


class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_date', 'end_date', 'last_updated',
    )


class AllocationActionAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'name', 'date', 'start_location', 'start_hour', 'end_location', 'end_hour'
    )


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(AllocationAction, AllocationActionAdmin)
