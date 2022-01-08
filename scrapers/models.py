import datetime
from calendar import monthrange

import icalendar
from dateutil.parser import parse as dateutil_parse
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone
from django.utils.dates import MONTHS
from django.utils.timezone import make_aware

from scrapers.backends import facade_authentication
from railroads.models import PublicRailroadTrain
from railroads.services import nearest_arriving_train, nearest_departing_train
from utils.dates import YEARS
from utils.icals import ICalComponentable, TriggeredAlarm
from utils.models import UUIDCommonModel

REQUEST_DATE_FMT = '%Y-%m-%d'


class AllocationTimetable(UUIDCommonModel):
    month = models.PositiveIntegerField('Miesiąc', default=timezone.now().month, choices=list(MONTHS.items()))
    year = models.PositiveIntegerField('Rok', default=timezone.now().year, choices=list(YEARS().items()))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Użytkownik', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Plan Służb'
        verbose_name_plural = 'Plany Służb'
        constraints = [
            models.CheckConstraint(check=Q(month__lte=12), name='month_lte_12'),
            models.UniqueConstraint(
                fields=['user_id', 'month', 'year'],
                name='unique_user_allocation_timetable',
            ),
        ]

    def __str__(self):
        return f'{self.month}-{self.year}'

    def __repr__(self):
        return f'AllocationTimetable({self.month}, {self.year}, {self.user})'

    def get_absolute_url(self):
        return reverse('allocation_timetable_detail', kwargs={'pk': self.pk})

    def get_date(self):
        return datetime.date(year=self.year, month=self.month, day=1)

    def add_related_objects_on_request(self, request):
        if self.allocation_set.exists():
            return self.allocation_set
        else:
            facade = facade_authentication(request)
            date = self.get_date().strftime(REQUEST_DATE_FMT)

            for data in facade.timetable_allocations(date):
                date = data['date']
                start_hour = data['start_hour']
                end_hour = data['end_hour']

                start_date = make_aware(dateutil_parse(f'{date} {start_hour}'))
                end_date = make_aware(dateutil_parse(f'{date} {end_hour}'))

                is_date_valid = start_date < end_date
                if not is_date_valid:
                    end_date += datetime.timedelta(days=1)

                allocation, _ = Allocation.objects.get_or_create(
                    title=data['title'], start_date=start_date, end_date=end_date
                )
                self.allocation_set.add(allocation)

            self.update_now()
            self.save()
            return self.allocation_set

    def update_related_objects_on_request(self, request):
        if self.allocation_set.exists():
            self.allocation_set.clear()
        return self.add_related_objects_on_request(request)

    @property
    def name(self):
        return f'Służby {self.month}-{self.year}'

    @property
    def days_in_month(self):
        days = monthrange(self.year, self.month)[1]
        return range(1, days + 1)


class Allocation(UUIDCommonModel, ICalComponentable):
    title = models.CharField('Tytuł', max_length=32)
    start_date = models.DateTimeField('Data rozpoczęcia')
    end_date = models.DateTimeField('Data zakończenia')

    timetable = models.ForeignKey(
        AllocationTimetable, verbose_name='Plan służb', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Służba"
        verbose_name_plural = "Służby"
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gte=F('start_date')), name='end_date_lte_start_date_check'
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

    def add_related_objects_on_request(self, request):
        if self.allocationdetail_set.exists():
            return self.allocationdetail_set
        else:
            facade = facade_authentication(request)
            date = self.start_date.strftime(REQUEST_DATE_FMT)

            for data in facade.allocation_details(title=self.title, date=date):
                start_hour = data['start_hour']
                action_date = make_aware(dateutil_parse(f'{date} {start_hour}'))
                is_action_date_correct = action_date >= self.start_date

                if not is_action_date_correct:
                    action_date += datetime.timedelta(days=1)

                detail, _ = AllocationDetail.objects.get_or_create(
                    action_date=action_date,
                    **data,
                )
                self.allocationdetail_set.add(detail)

            self.update_now()
            self.save()
            return self.allocationdetail_set

    def update_related_objects_on_request(self, request):
        if self.allocationdetail_set.exists():
            self.allocationdetail_set.clear()
        return self.add_related_objects_on_request(request)

    def get_as_ical_component(self):
        cal = icalendar.Calendar()
        event = icalendar.Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)

        alarm = TriggeredAlarm(hours=12)
        event.add_component(alarm)

        description = ""
        for detail in self.allocationdetail_set.all():
            description += f'{detail.ical_description()} \n'
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
        PublicRailroadTrain, verbose_name='Pociąg przed służbą', related_name='before',
        null=True, blank=True, on_delete=models.CASCADE
    )
    after = models.OneToOneField(
        PublicRailroadTrain, verbose_name='Pociąg po służbie', related_name='after',
        null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Pociąg dla służby'
        verbose_name_plural = 'Pociągi dla służb'

    def __str__(self):
        return f'Pociągi dla {self.allocation}, przed: {self.before}, po: {self.after}.'

    def __repr__(self):
        return f'AllocationTrain({repr(self.allocation)}, {repr(self.before)}, {repr(self.after)})'

    def search_before(self, departure_station, arrival_station, spare_time=10):
        date = self.allocation.start_date - datetime.timedelta(minutes=int(spare_time))
        train = nearest_arriving_train(date, departure_station, arrival_station)
        self.before = train
        self.save()
        return self.before

    def search_after(self, departure_station, arrival_station, spare_time=10):
        date = self.allocation.end_date + datetime.timedelta(minutes=int(spare_time))
        train = nearest_departing_train(date, departure_station, arrival_station)
        self.after = train
        self.save()
        return self.after


class AllocationDetail(models.Model):
    train_number = models.CharField('Numer pociągu', max_length=32, null=True)
    action_date = models.DateTimeField('Data akcji', null=True)
    action = models.CharField('Akcja', max_length=128, null=True)
    start_location = models.CharField('Lokalizacja początkowa', max_length=128, null=True)
    start_hour = models.CharField('Godzina', max_length=32, null=True)
    end_location = models.CharField('Lokalizacja końcowa', max_length=128, null=True)
    end_hour = models.CharField('Godzina', max_length=32, null=True)

    allocation = models.ForeignKey(
        Allocation, verbose_name='Służba', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Detail służby'
        verbose_name_plural = 'Detale służb'
        ordering = ['action_date']

    def __str__(self):
        return f"""
        {self.train_number} {self.action}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """

    def ical_description(self):
        if self.train_number:
            return f"""{self.train_number} {self.action}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """
        else:
            return f"""{self.action}
        {self.start_location} {self.start_hour} 
        {self.end_location} {self.end_hour}
        """


class TrainCrew(UUIDCommonModel):
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
    def date_as_datetime(self):
        fmt = '%Y-%m-%d'
        date = make_aware(datetime.datetime.strptime(self.date, fmt))
        return date

    def add_related_objects_on_request(self, request):
        if self.traincrewmember_set.exists():
            return self.traincrewmember_set
        else:
            facade = facade_authentication(request)
            for data in facade.train_crew(self.train_number, self.date):
                crew_member, _ = TrainCrewMember.objects.get_or_create(**data)
                self.traincrewmember_set.add(crew_member)

            self.update_now()
            self.save()
            return self.traincrewmember_set

    def update_related_objects_on_request(self, request):
        if self.traincrewmember_set.exists():
            self.traincrewmember_set.clear()
        return self.add_related_objects_on_request(request)


class TrainCrewMember(UUIDCommonModel):
    crew = models.ForeignKey(
        TrainCrew, verbose_name="Członek załogi", related_query_name='members', on_delete=models.CASCADE,
        null=True, blank=True
    )
    person = models.CharField('Osoba', max_length=128)
    phone_number = models.CharField('Numer telefonu', max_length=32, null=True, blank=True)
    profession = models.CharField('Stanowisko', max_length=32)
    start_location = models.CharField('Lokalizacja początkowa', max_length=32)
    end_location = models.CharField('Lokalizacja końcowa', max_length=32)

    class Meta:
        verbose_name = 'Członek załogi pociągu'
        verbose_name_plural = 'Członkowie załogi pociągów'

    def __str__(self):
        return f"""
        {self.person}, {self.profession}, {self.phone_number},
        {self.start_location}, {self.end_location}
        """
