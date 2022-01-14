import datetime
from calendar import monthrange

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.dates import MONTHS

from IVU.api.requests import IVURequestWithDateValue
from IVU.timetables.managers import TimetableManager
from dates.models import UUIDTimestampedModel
from dates.years import YEARS


class Timetable(UUIDTimestampedModel):
    month = models.PositiveIntegerField('Miesiąc', default=timezone.now().month, choices=list(MONTHS.items()))
    year = models.PositiveIntegerField('Rok', default=timezone.now().year, choices=list(YEARS().items()))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Użytkownik', null=True, blank=True, on_delete=models.CASCADE
    )

    objects = TimetableManager()

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plany'
        constraints = [
            models.CheckConstraint(check=Q(month__lte=12), name='month_lte_12'),
            models.UniqueConstraint(
                fields=['user_id', 'month', 'year'],
                name='unique_allocation_timetable_for_user',
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
    def calendar_name(self):
        return f'Służby {self.month}-{self.year}'

    @property
    def days_in_month(self):
        days = monthrange(self.year, self.month)[1]
        return range(1, days + 1)

    @property
    def attrs_dict(self):
        return {'date': self.date.strftime(IVURequestWithDateValue.fmt)}
