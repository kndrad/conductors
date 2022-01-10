import datetime
from calendar import monthrange

import icalendar
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone
from django.utils.dates import MONTHS

from IVU.requests import IVUDatedRequest
from transports.models import PublicTrain
from utils.dates import YEARS
from utils.icals import ICalComponentable, TriggeredAlarm
from utils.models import UUIDModel, UUIDTimestampedModel


class Timetable(UUIDTimestampedModel):
    month = models.PositiveIntegerField('Miesiąc', default=timezone.now().month, choices=list(MONTHS.items()))
    year = models.PositiveIntegerField('Rok', default=timezone.now().year, choices=list(YEARS().items()))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Użytkownik', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plany'
        constraints = [
            models.CheckConstraint(check=Q(month__lte=12), name='month_lte_12'),
            models.UniqueConstraint(
                fields=['user_id', 'month', 'year'],
                name='unique_timetable_for_user',
            ),
        ]

    def __str__(self):
        return f'{self.month}-{self.year}'

    def __repr__(self):
        return f'Timetable({self.month}, {self.year}, {self.user})'

    def get_absolute_url(self):
        return reverse('timetable_detail', kwargs={'pk': self.pk})

    @property
    def date(self):
        return datetime.date(year=self.year, month=self.month, day=1)

    @property
    def name(self):
        return f'Służby {self.month}-{self.year}'

    @property
    def days_in_month(self):
        days = monthrange(self.year, self.month)[1]
        return range(1, days + 1)


class Allocation(UUIDTimestampedModel, ICalComponentable):
    title = models.CharField('Tytuł', max_length=32)
    signature = models.CharField('Sygnatura', max_length=64)
    start_date = models.DateTimeField('Data rozpoczęcia')
    end_date = models.DateTimeField('Data zakończenia')

    timetable = models.ForeignKey(
        Timetable, verbose_name='Plan', null=True, blank=True, on_delete=models.CASCADE
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

    def __str__(self):
        fmt = '%H:%M'
        start_date_local = timezone.localtime(self.start_date).strftime(fmt)
        end_date_local = timezone.localtime(self.end_date).strftime(fmt)
        return f'{start_date_local} {self.title} {end_date_local}'

    def __repr__(self):
        return f'Allocation({self.title}, {self.start_date}, {self.end_date})'

    def get_absolute_url(self):
        return reverse('allocation_detail', kwargs={'pk': self.pk})

    def start_day(self):
        return int(self.start_date.day)

    def to_ical_component(self):
        cal = icalendar.Calendar()
        event = icalendar.Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)

        alarm = TriggeredAlarm(hours=12)
        event.add_component(alarm)

        description = ""
        for action in self.action_set.all():
            description += f'{action.ical_description} \n'

        event.add('description', description)
        cal.add_component(event)
        return cal

    @property
    def is_month_old(self):
        days = 30
        month_ago = timezone.now() - datetime.timedelta(days=days)
        return month_ago > self.start_date


class Action(models.Model):
    train_number = models.CharField('Numer pociągu', max_length=32, null=True)
    date = models.DateTimeField('Data', null=True)
    name = models.CharField('Nazwa', max_length=128, null=True)
    start_location = models.CharField('Lokalizacja początkowa', max_length=128, null=True)
    start_hour = models.CharField('Godzina', max_length=32, null=True)
    end_location = models.CharField('Lokalizacja końcowa', max_length=128, null=True)
    end_hour = models.CharField('Godzina', max_length=32, null=True)

    allocation = models.ForeignKey(
        Allocation, verbose_name='Służba', null=True, blank=True, on_delete=models.CASCADE
    )

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
