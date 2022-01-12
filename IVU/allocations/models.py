import datetime

import icalendar
from django.db import models
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone

from IVU.api.requests import IVURequestWithDateValue
from IVU.timetables.models import Timetable
from trains.models import Train
from utils.icals import ICalComponentable, TriggeredAlarm
from dates.models import UUIDTimestampedModel


class Allocation(UUIDTimestampedModel, ICalComponentable):
    title = models.CharField('Tytuł', max_length=32)
    signature = models.CharField('Sygnatura', max_length=64)
    start_date = models.DateTimeField('Rozpoczęcie')
    end_date = models.DateTimeField('Zakończenie')

    timetable = models.ForeignKey(
        Timetable, related_name='allocations', verbose_name='Plan', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Służba'
        verbose_name_plural = 'Służby'
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gte=F('start_date')), name='check_end_date_lte_start_date'
            ),
        ]
        ordering = ['start_date']

    query_name = 'allocations'

    def __str__(self):
        fmt = '%H:%M'
        start_date = timezone.localtime(self.start_date).strftime(fmt)
        end_date = timezone.localtime(self.end_date).strftime(fmt)
        return f'{start_date} {self.title} {end_date}'

    def __repr__(self):
        return f'Allocation({self.title}, {self.start_date}, {self.end_date})'

    def get_absolute_url(self):
        return reverse('allocation_detail', kwargs={'pk': self.pk})

    @property
    def start_day(self):
        return int(self.start_date.day)

    @property
    def resource_kwargs(self):
        return {
            'title': self.title,
            'date': self.start_date.strftime(IVURequestWithDateValue.fmt)
        }

    def to_ical_component(self):
        cal = icalendar.Calendar()
        event = icalendar.Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)

        alarm = TriggeredAlarm(hours=12)
        event.add_component(alarm)

        description = ""
        for action in self.actions.all():
            description += f'{action.ical_description} \n'

        event.add('description', description)
        cal.add_component(event)
        return cal

    @property
    def is_month_old(self):
        days = 30
        month_ago = timezone.now() - datetime.timedelta(days=days)
        return month_ago > self.start_date


class AllocationTrain(models.Model):
    allocation = models.OneToOneField(
        Allocation, verbose_name='Pociąg dla służby', related_name='train',
        null=True, blank=True, on_delete=models.CASCADE
    )
    before = models.OneToOneField(
        Train, verbose_name='Przed', related_name='before',
        null=True, blank=True, on_delete=models.CASCADE
    )
    after = models.OneToOneField(
        Train, verbose_name='Po', related_name='after',
        null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Pociąg dla służby'
        verbose_name_plural = 'Pociągi dla służb'

    def __str__(self):
        return f'Pociągi dla {self.allocation}, przed: {self.before}, po: {self.after}.'

    def __repr__(self):
        return f'AllocationTrain({repr(self.allocation)}, {repr(self.before)}, {repr(self.after)})'


class AllocationAction(models.Model):
    train_number = models.CharField('Numer pociągu', max_length=32, null=True)
    date = models.DateTimeField('Data', null=True)
    name = models.CharField('Nazwa', max_length=128, null=True)
    start_location = models.CharField('Lokalizacja początkowa', max_length=128, null=True)
    start_hour = models.CharField('Godzina', max_length=32, null=True)
    end_location = models.CharField('Lokalizacja końcowa', max_length=128, null=True)
    end_hour = models.CharField('Godzina', max_length=32, null=True)

    allocation = models.ForeignKey(
        Allocation, verbose_name='Służba', related_name='actions', null=True, blank=True, on_delete=models.CASCADE
    )

    query_name = 'actions'

    class Meta:
        verbose_name = 'Akcja'
        verbose_name_plural = 'Akcje'
        ordering = ['date']

    def __str__(self):
        return f"""
        {self.train_number} {self.name}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """

    @property
    def date_string(self):
        return timezone.localtime(self.date).strftime(IVURequestWithDateValue.fmt)

    @property
    def ical_description(self):
        if self.train_number:
            return f"""{self.train_number} {self.name}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """
        else:
            return f"""{self.name}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """
