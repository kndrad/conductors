import icalendar
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone

from utils.icals import ICalComponentable, TriggeredAlarm
from dates.models import UUIDModel


class RailroadAccount(UUIDModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name='Konto kolejowe',
        related_name='railroad_account', null=True, blank=True, on_delete=models.CASCADE
    )
    homeplace = models.CharField('Stacja kolejowa w miejscu zamieszkania', max_length=64)
    workplace = models.CharField('Stacja kolejowa w miejscu pracy', max_length=64)

    class SpareTime(models.IntegerChoices):
        VERY_SHORT = 10, '10 minut'
        SHORT = 20, '20 minut'
        MEDIUM = 30, '30 minut'
        LONG = 40, '40 minut'
        VERY_LONG = 50, '50 minut'
        LONGEST = 60, '60 minut'

    administration_time = models.PositiveIntegerField(
        'Czas administracyjny', choices=SpareTime.choices, default=SpareTime.VERY_SHORT
    )

    class Meta:
        verbose_name = 'Konto kolejowe'
        verbose_name_plural = 'Konta kolejowe'

        constraints = [
            models.CheckConstraint(
                check=~Q(homeplace__iexact=F('workplace')), name='homeplace_not_eq_workplace'
            ),
        ]

    def __str__(self):
        return f'{self.user}, [{self.homeplace}, {self.workplace}]'

    def __repr__(self):
        return f'RailroadAccount({self.user}, {self.homeplace}, {self.workplace})'


class VerifiedStation(models.Model):
    name = models.CharField('Nazwa', max_length=64, unique=True)

    class Meta:
        verbose_name = 'Zweryfikowana stacja'
        verbose_name_plural = 'Zweryfikowane stacje'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'VerifiedStation({self.name})'


class Train(models.Model, ICalComponentable):
    number = models.CharField('Numer', max_length=64)
    carrier = models.CharField('Przewoźnik', max_length=64, null=True, blank=True)

    departure_date = models.DateTimeField('Czas odjazdu')
    departure_station = models.CharField('Odjazd ze stacji', max_length=64)
    departure_platform = models.CharField('Odjazd z peronu', max_length=32)

    arrival_date = models.DateTimeField('Czas przyjazdu')
    arrival_station = models.CharField('Przyjazd na stację', max_length=64)
    arrival_platform = models.CharField('Przyjazd na peron', max_length=32)

    class Meta:
        verbose_name = 'Pociąg'
        verbose_name_plural = 'Pociągi'

    def __str__(self):
        fmt = '%H:%M'
        local_departure_date = timezone.localtime(self.departure_date)
        departure_hour = local_departure_date.strftime(fmt)
        local_arrival_date = timezone.localtime(self.arrival_date)
        arrival_hour = local_arrival_date.strftime(fmt)
        return f'{departure_hour} {self.carrier_initials} {self.number} {arrival_hour}'

    def __repr__(self):
        return f"""
        Train({self.number}, {self.carrier}, 
        {self.departure_station}, {self.departure_platform}, {self.departure_date}, 
        {self.arrival_station}, {self.arrival_platform}, {self.arrival_date})
        """

    def get_absolute_url(self):
        return reverse('train_detail', kwargs={'pk': self.pk})

    @property
    def departure_day(self):
        return self.departure_date.day

    @property
    def carrier_initials(self):
        if not self.carrier:
            return
        if 'PKP' in self.carrier:
            return 'PKP'
        names = self.carrier.split()
        try:
            return "".join([names[0][0], names[1][0]])
        except IndexError:
            return self.carrier

    @property
    def summary(self):
        return f'{self.carrier_initials} {self.number} | {self.departure_station.title()} -> {self.arrival_station.title()}'

    def to_ical_component(self):
        cal = icalendar.Calendar()
        event = icalendar.Event()
        summary = (
            f'{self.carrier_initials} {self.number} | {self.departure_station.title()} -> {self.arrival_station.title()}'
        )
        event.add('summary', summary)
        event.add('dtstart', self.departure_date)
        for alarm in [TriggeredAlarm(hours=2), TriggeredAlarm(minutes=30)]:
            event.add_component(alarm)
        event.add('dtend', self.arrival_date)
        description = (
            f'{self.carrier}\n'
            f'Odjazd z peronu: {self.departure_platform}\n'
            f'Przyjazd na peron: {self.arrival_platform}\n'
        )
        event.add('description', description)
        cal.add_component(event)
        return cal
