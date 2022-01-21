import datetime
from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import Allocation, AllocationAction


class AllocationModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        start_date = make_aware(datetime.datetime(year=2022, month=1, day=21, hour=15, minute=52))
        end_date = start_date + timedelta(hours=12)
        kwargs = {
            'title': 'KKA320',
            'start_date': start_date,
            'end_date': end_date
        }
        cls.obj = Allocation.objects.create(**kwargs)
        cls.obj_dict = kwargs

    def test_start_day_property(self):
        self.assertEqual(self.obj.start_day, 21)

    def test_date_for_api_property(self):
        self.assertEqual(self.obj.date_for_api, '2022-01-21')

    def test_start_date_gt_end_date_check_constraint(self):
        kwargs = self.obj_dict
        kwargs['end_date'] -= timedelta(hours=13)  # one hour lower than initial start_date

        obj = Allocation(**kwargs)
        with self.assertRaises(IntegrityError):
            obj.save()

    def test_is_month_old_property(self):
        start_date = timezone.now() - timedelta(days=32)
        kwargs = {
            'title': self.obj_dict['title'],
            'start_date': start_date,
            'end_date': start_date + timedelta(hours=8)
        }
        obj = Allocation.objects.create(**kwargs)
        self.assertTrue(obj.is_month_old)  # should be True, because start_date of an object was 32 days ago.

        start_date = timezone.now() + timedelta(days=1)
        kwargs = {
            'title': self.obj_dict['title'],
            'start_date': start_date,
            'end_date': start_date + timedelta(hours=8)
        }

        obj = Allocation.objects.create(**kwargs)
        self.assertFalse(obj.is_month_old)  # should be False, because start_date of an object will be tomorrow.


class AllocationActionModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        date = make_aware(datetime.datetime(year=2022, month=1, day=21, hour=12))
        cls.obj = AllocationAction.objects.create(date=date)
        cls.obj_date = date

    def test_date_for_api_property(self):
        self.assertEqual(self.obj.date_for_api, '2022-01-21')

