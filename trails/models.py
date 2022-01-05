from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.utils import timezone

from utils.fields import LowercaseCharField


class TrailStation(models.Model):
    name = LowercaseCharField('Nazwa stacji', max_length=128)

    class Meta:
        verbose_name = 'Stacja na szlaku'
        verbose_name_plural = 'Stacje na szlaku'

    def __repr__(self):
        return f'TrailStation({self.name})'

    def __str__(self):
        return self.name.title()


class Trail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Użytkownik', on_delete=models.CASCADE)
    beginning = models.CharField('Początek szlaku', max_length=128)
    finale = models.CharField('Koniec szlaku', max_length=128)
    last_driven = models.DateField('Data ostatniego przejazdu', default=timezone.now)
    stations_through = models.ManyToManyField(TrailStation, verbose_name='Stacje na szlaku', blank=True)

    class Meta:
        verbose_name = 'Szlak'
        verbose_name_plural = 'Szlaki'
        constraints = [
            models.CheckConstraint(
                check=~Q(beginning=F('finale')),
                name='trail_beginning_and_finale_can_not_be_equal')
        ]

    def __repr__(self):
        return f'Trail({self.user},{self.beginning},{self.finale},{self.last_driven})'

    def __str__(self):
        stations = [str(station) for station in self.stations_through.all()]
        return f'Szlak od {self.beginning} do {self.finale}, przez {stations}'

    @property
    def expiration_months(self):
        return 12

    @property
    def expiration_date(self):
        """By now, expiraton date for a trail is defined in this class as a property.
        """
        months = self.expiration_months
        expiration_date = self.last_driven + relativedelta(months=+months)
        return timezone.localtime(expiration_date)

    @property
    def annonucement_date(self):
        """Annoucement date for a dispatcher from an user when trail is going to expire.
        It is less than expiration months value.
        """
        factor = 2
        months = self.expiration_months - factor
        announcement_date = self.expiration_date - relativedelta(months=-months)
        return timezone.localtime(announcement_date)
