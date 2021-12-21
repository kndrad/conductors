import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class TicketProlongation(models.Model):
    class Ticket(models.TextChoices):
        FINE = ('FINE', 'Wezwanie do zapłaty')
        BLANKET = ('BLANKET', 'Blankietowy')
        REPLACEMENT = ('REPLACEMENT', 'Zastępczy')

    ticket = models.CharField('Bilet', choices=Ticket.choices, max_length=128, default=Ticket.FINE)
    last_renewal_date = models.DateField(verbose_name='Data ostatniego przedłużenia', default=timezone.now)
    expiration_date = models.DateField(verbose_name='Data wygaśnięcia', editable=False, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Użytkownik', on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Prolongata Biletu'
        verbose_name_plural = 'Prolongaty Biletów'

        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'ticket'],
                name='unique_user_ticket_prolongation',
            ),
        ]

    def __repr__(self):
        return f'{self.__class__.__name__}({self.ticket}, {self.last_renewal_date})'

    def __str__(self):
        return f'{self.ticket}'

    def get_absolute_url(self):
        return reverse('ticket_prolongations', kwargs={'pk':  self.user.pk})

    def save(self, *args, **kwargs):
        self.clean_fields()

        last_renewal = self.last_renewal_date
        self.expiration_date = last_renewal + datetime.timedelta(days=30)

        return super().save(*args, **kwargs)

    @property
    def days_until_expiration(self):
        now = timezone.now().date()
        date = self.expiration_date - now
        return abs(date.days)

    def get_expiration_message(self):
        days = self.days_until_expiration
        if days == 1:
            return 'Wygasa za 1 dzień'
        else:
            return f'Wygasa za {days} dni'




