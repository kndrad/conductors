from django.contrib import admin

from .models import Prolongation


class TicketProlongationAdmin(admin.ModelAdmin):
    list_display = (
        'ticket', 'last_renewal_date', 'expiration_date', 'user',
    )


admin.site.register(Prolongation, TicketProlongationAdmin)
