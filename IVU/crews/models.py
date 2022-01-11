import datetime

from django.db import models
from django.utils.timezone import make_aware

from utils.models import UUIDModel


class Crew(UUIDModel):
    trip = models.CharField('Number pociągu', max_length=32)
    date = models.CharField('Data', max_length=32)

    class Meta:
        verbose_name = 'Załoga pociągu'
        verbose_name_plural = 'Załogi pociągów'

    def __str__(self):
        return f'{self.trip}, {self.date}'

    def __repr__(self):
        return f'TripCrew({self.trip}, {self.date})'

    @property
    def date_as_datetime(self):
        fmt = '%Y-%m-%d'
        date = make_aware(datetime.datetime.strptime(self.date, fmt))
        return date


class Member(UUIDModel):
    crew = models.ForeignKey(
        Crew, verbose_name='Członek załogi', on_delete=models.CASCADE, null=True, blank=True
    )
    person = models.CharField('Osoba', max_length=128)
    phone = models.CharField('Telefon', max_length=32, null=True, blank=True)
    profession = models.CharField('Stanowisko', max_length=32)
    start_location = models.CharField('Lokalizacja początkowa', max_length=32)
    end_location = models.CharField('Lokalizacja końcowa', max_length=32)

    class Meta:
        verbose_name = 'Członek załogi pociągu'
        verbose_name_plural = 'Członkowie załogi pociągów'

    def __str__(self):
        return f"""
        {self.person}, {self.profession}, {self.phone},
        {self.start_location}, {self.end_location}
        """
