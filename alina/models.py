import datetime

from dateutil.parser import parse as dateutil_parse
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone
from django.utils.dates import MONTHS
from django.utils.timezone import make_aware

from alina.interface import Alina
from alina.tools.utils import credentials_from_request, parse_alina_date
from alina.tools.utils import parse_alina_timetable_date
from utils.dates import YEARS
from utils.models import UUIDCommonModel

VIEW_DATE_FORMAT = "%H:%M %d.%m.%Yr."


class AllocationTimetable(UUIDCommonModel):
    month = models.PositiveIntegerField(
        verbose_name='Miesiąc', default=timezone.now().month, choices=list(MONTHS.items())
    )
    year = models.PositiveIntegerField(
        verbose_name='Rok', default=timezone.now().year, choices=list(YEARS().items())
    )

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
        return reverse('allocation_timetable_allocations', kwargs={'pk': self.user.pk})

    def add_allocations_on_request(self, request):
        if self.allocation_set.exists():
            return self.allocation_set
        else:
            email, password = credentials_from_request(request)

            alina = Alina(email, password)
            formatted_date = parse_alina_timetable_date(self)
            parsed_allocations = alina.timetable_allocations(formatted_date)

            for parsed_allocation_data in parsed_allocations:
                date = parsed_allocation_data['date']
                start_hour = parsed_allocation_data['start_hour']
                end_hour = parsed_allocation_data['end_hour']

                start_date = make_aware(dateutil_parse(f'{date} {start_hour}'))
                end_date = make_aware(dateutil_parse(f'{date} {end_hour}'))

                is_date_valid = start_date < end_date
                if not is_date_valid:
                    end_date += datetime.timedelta(days=1)

                allocation, _ = Allocation.objects.get_or_create(
                    title=parsed_allocation_data['title'], start_date=start_date, end_date=end_date
                )
                self.allocation_set.add(allocation)

            self.updated_now()
            self.save()
            return self.allocation_set

    def update_allocations_on_request(self, request):
        if self.allocation_set.exists():
            self.allocation_set.clear()
        return self.add_allocations_on_request(request)


class Allocation(UUIDCommonModel):
    title = models.CharField(verbose_name='Tytuł', max_length=32)
    start_date = models.DateTimeField(verbose_name='Data rozpoczęcia')
    end_date = models.DateTimeField(verbose_name='Data zakończenia')

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
        start_date_local = timezone.localtime(self.start_date).strftime(VIEW_DATE_FORMAT)
        end_date_local = timezone.localtime(self.end_date).strftime(VIEW_DATE_FORMAT)
        return f'{start_date_local} {self.title} {end_date_local}'

    def __repr__(self):
        return f'Allocation({self.title}, {self.start_date}, {self.end_date})'

    def get_absolute_url(self):
        return reverse('allocation_details', kwargs={'pk': self.pk})

    def add_details_on_request(self, request):
        if self.allocationdetail_set.exists():
            return self.allocationdetail_set
        else:
            email, password = credentials_from_request(request)
            alina = Alina(email, password)
            date = parse_alina_date(self.start_date)
            parsed_details = alina.allocation_details(title=self.title, date=date)

            for parsed_detail_data in parsed_details:
                start_hour = parsed_detail_data['start_hour']
                action_date = make_aware(dateutil_parse(f'{date} {start_hour}'))
                is_action_date_correct = action_date >= self.start_date

                if not is_action_date_correct:
                    action_date += datetime.timedelta(days=1)

                detail, _ = AllocationDetail.objects.get_or_create(
                    train_number=parsed_detail_data['train_number'],
                    action_date=action_date,
                    action=parsed_detail_data['action'],
                    start_location=parsed_detail_data['start_location'],
                    start_hour=start_hour,
                    end_location=parsed_detail_data['end_location'],
                    end_hour=parsed_detail_data['end_hour']
                )
                self.allocationdetail_set.add(detail)

            self.updated_now()
            self.save()
            return self.allocationdetail_set

    def update_details_on_request(self, request):
        if self.allocationdetail_set.exists():
            self.allocationdetail_set.clear()
        return self.add_details_on_request(request)


class AllocationDetail(models.Model):
    train_number = models.CharField(verbose_name='Number pociągu', max_length=32, null=True)
    action_date = models.DateTimeField(verbose_name='Data akcji', null=True)
    action = models.CharField(verbose_name='Akcja', max_length=128, null=True)
    start_location = models.CharField(verbose_name='Lokalizacja początkowa', max_length=128, null=True)
    start_hour = models.CharField(verbose_name='Godzina', max_length=32, null=True)
    end_location = models.CharField(verbose_name='lokalizacja końcowa', max_length=128, null=True)
    end_hour = models.CharField(verbose_name='Godzina', max_length=32, null=True)

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

    @property
    def formatted_action_date(self):
        formatted_action_date = parse_alina_date(self.action_date)
        return formatted_action_date


class TrainCrew(UUIDCommonModel):
    train_number = models.CharField(verbose_name='Numer pociągu', max_length=32)
    date = models.CharField(verbose_name='Data', max_length=32)

    class Meta:
        verbose_name = 'Załoga pociągu'
        verbose_name_plural = 'Załogi pociągów'

    def __str__(self):
        return f'{self.train_number}, {self.date}'

    def __repr__(self):
        return f'TrainCrew({self.train_number}, {self.date})'

    def add_members_on_request(self, request):
        if self.traincrewmember_set.exists():
            return self.traincrewmember_set
        else:
            email, password = credentials_from_request(request)
            alina = Alina(email, password)
            parsed_crew_members = alina.train_crew(self.train_number, self.date)

            for parsed_member_data in parsed_crew_members:
                crew_member, _ = TrainCrewMember.objects.get_or_create(
                    person=parsed_member_data['person'],
                    phone_number=parsed_member_data['phone_number'],
                    profession=parsed_member_data['profession'],
                    start_location=parsed_member_data['start_location'],
                    end_location=parsed_member_data['end_location'],
                )
                self.traincrewmember_set.add(crew_member)

            self.updated_now()
            self.save()
            return self.traincrewmember_set

    def update_members_on_request(self, request):
        if self.traincrewmember_set.exists():
            self.traincrewmember_set.clear()
        return self.add_members_on_request(request)


class TrainCrewMember(UUIDCommonModel):
    crew = models.ForeignKey(
        TrainCrew, verbose_name="Członek załogi", related_query_name='members', on_delete=models.CASCADE,
        null=True, blank=True
    )
    person = models.CharField(max_length=128, verbose_name='Osoba')
    phone_number = models.CharField(max_length=32, verbose_name='Numer telefonu')
    profession = models.CharField(max_length=32, verbose_name='Stanowisko')
    start_location = models.CharField(max_length=32, verbose_name='Lokalizacja początkowa')
    end_location = models.CharField(max_length=32, verbose_name='Lokalizacja końcowa')

    class Meta:
        verbose_name = 'Członek załogi pociągu'
        verbose_name_plural = 'Członkowie załogi pociągu'

    def __str__(self):
        return f"""
        {self.person}, {self.profession}, {self.phone_number},
        {self.start_location}, {self.end_location}
        """