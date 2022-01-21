from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from IVU.timetables.models import Timetable


class TimetableModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        obj = Timetable.objects.create(month=1, year=2022)
        cls.obj = obj

    def test_invalid_timetable_month_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Timetable.objects.create(month=13, year=2021)

    def test_creating_two_identical_timetables_for_same_user_raises_integrity_error(self):
        user = get_user_model().objects.create(email='test.email@domain.com')

        month, year = 12, 2021
        Timetable.objects.create(user=user, month=month, year=year)
        with self.assertRaises(IntegrityError):
            Timetable.objects.create(user=user, month=month, year=year)

    def test_days_in_month_property(self):
        days = range(1, 32)  # 31 objects
        self.assertEqual(self.obj.days_in_month, days)

    def test_date_for_api_property(self):
        self.assertEqual(self.obj.date_for_api, '2022-01-01')
