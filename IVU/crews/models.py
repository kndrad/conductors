import datetime

from django.db import models
from django.utils.timezone import make_aware

from dates.models import UUIDModel


class TrainCrew(UUIDModel):
    train_number = models.CharField('Numer pociągu', max_length=32)
    date = models.CharField('Data', max_length=32)

    class Meta:
        verbose_name = 'Załoga pociągu'
        verbose_name_plural = 'Załogi pociągów'

    def __str__(self):
        return f'{self.train_number}, {self.date}'

    def __repr__(self):
        return f'TrainCrew({self.train_number}, {self.date})'

    @property
    def datetime(self):
        date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        return make_aware(date)


class TrainCrewMember(UUIDModel):
    crew = models.ForeignKey(
        TrainCrew, verbose_name='Członek załogi', related_name='members', on_delete=models.CASCADE,
        null=True, blank=True
    )
    person = models.CharField('Osoba', max_length=128)
    phone = models.CharField('Telefon', max_length=32, null=True, blank=True)
    profession = models.CharField('Stanowisko', max_length=32)
    start_location = models.CharField('Lokalizacja początkowa', max_length=32)
    end_location = models.CharField('Lokalizacja końcowa', max_length=32)

    query_name = 'members'

    class Meta:
        verbose_name = 'Członek załogi pociągu'
        verbose_name_plural = 'Członkowie załogi pociągów'

    def __str__(self):
        return f'{self.person}, {self.profession}, {self.phone},{self.start_location}, {self.end_location}'
