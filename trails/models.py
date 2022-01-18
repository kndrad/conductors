from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.utils import timezone

from common.fields import LowerCaseCharField
from .validators import sentence_validator


class Waypoint(models.Model):
    name = LowerCaseCharField('Nazwa', max_length=128, validators=[sentence_validator])

    class Meta:
        verbose_name = 'Punkt na szlaku'
        verbose_name_plural = 'Punkty na szlaku'

    def __repr__(self):
        return f'Waypoint({self.name})'

    def __str__(self):
        return self.name.title()


class Trail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Użytkownik', on_delete=models.CASCADE)
    start = models.CharField('Stacja początkowa', validators=[sentence_validator], max_length=128)
    end = models.CharField('Stacja końcowa', validators=[sentence_validator], max_length=128)
    last_driven = models.DateField('Data ostatniego przejazdu', default=timezone.now)
    waypoints = models.ManyToManyField(Waypoint, related_name='waypoints', verbose_name='Punkty na szlaku', blank=True)

    class Meta:
        verbose_name = 'Szlak'
        verbose_name_plural = 'Szlaki'
        constraints = [
            models.CheckConstraint(
                check=~Q(start=F('end')),
                name='trail_start_cannot_be_equal_end')
        ]

    def __repr__(self):
        return f'Trail({self.user},{self.start},{self.end},{self.last_driven})'

    def __str__(self):
        waypoints = [str(waypoint) for waypoint in self.waypoints.all()]
        return f'Szlak: {self.start} -> {self.end}, przez {waypoints}'

    EXPIRATION_MONTHS = 12

    @property
    def expiration_date(self):
        """By now, expiraton date for a trail is defined in this class.
        """
        months = self.EXPIRATION_MONTHS
        expiration_date = self.last_driven + relativedelta(months=+months)
        return timezone.localtime(expiration_date)

    @property
    def annonucement_date(self):
        """Annoucement date for a dispatcher from an user when trail is going to expire.
        It is less than expiration months value.
        """
        factor = 2
        months = self.EXPIRATION_MONTHS - factor
        announcement_date = self.expiration_date - relativedelta(months=-months)
        return timezone.localtime(announcement_date)
