import datetime

import icalendar
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from icals import ICalConvertable, ICalTriggeredAlarm


class Prolongation(models.Model, ICalConvertable):
    class Ticket(models.TextChoices):
        FINE = ('FINE', 'Wezwania do zapłaty')
        BLANKET = ('BLANKET', 'Bilety blankietowe')

    ticket = models.CharField('Bilety', choices=Ticket.choices, max_length=128, default=Ticket.FINE)
    last_renewal_date = models.DateField(verbose_name='Data ostatniego przedłużenia', default=timezone.now)
    expiration_date = models.DateField(verbose_name='Data wygaśnięcia', editable=False, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Użytkownik', on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Prolongata'
        verbose_name_plural = 'Prolongaty'

        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'ticket'],
                name='unique_user_prolongation',
            ),
        ]

    def __repr__(self):
        return f'{self.__class__.__name__}({self.ticket}, {self.last_renewal_date})'

    def __str__(self):
        return f'{self.ticket}'

    def get_absolute_url(self):
        return reverse('prolongation_list', kwargs={'pk':  self.user.pk})

    DEFAULT_EXPIRATION = {'days': 30}

    def save(self, *args, **kwargs):
        self.clean_fields()
        self.expiration_date = self.last_renewal_date + datetime.timedelta(**self.DEFAULT_EXPIRATION)
        return super().save(*args, **kwargs)

    @property
    def days_until_expiration(self):
        return self.expiration_date - timezone.now().date()

    def get_expiration_message(self):
        days = self.days_until_expiration.days

        if days < 0:
            return 'Prolongata wygasła.'
        elif days == 0:
            return 'Prolongata wygasa dzisiaj!'
        elif days == 1:
            return 'Wygaśnie jutro.'
        else:
            return f'Wygaśnie za {days} dni.'

    def to_ical_component(self):
        cal = icalendar.Calendar()
        event = icalendar.Event()
        event.add('summary', self.get_ticket_display())
        event.add('dtstart', self.expiration_date)
        event.add('dtend', self.expiration_date)

        alarms = [ICalTriggeredAlarm(days=7), ICalTriggeredAlarm(days=3), ICalTriggeredAlarm(hours=8)]
        for alarm in alarms:
            event.add_component(alarm)

        event.add('description', 'Prolongata')
        cal.add_component(event)
        return cal




