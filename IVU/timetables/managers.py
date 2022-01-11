from datetime import timedelta

from django.db import models
from django.utils import timezone


class TimetableManager(models.Manager):

    def create_present_on_request(self, request):
        date = timezone.now()
        timetable, created = self.model.objects.get_or_create(
            user=request.user, month=date.month, year=date.year
        )
        return timetable

    def create_future_on_request(self, request):
        days = 30
        date = timezone.now() + timedelta(days=days)
        timetable, created = self.model.objects.get_or_create(
            user=request.user, month=date.month, year=date.year
        )
        return timetable
