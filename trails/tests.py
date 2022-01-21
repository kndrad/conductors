from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from trails.models import Trail, Waypoint
from .validators import validate_sentence

class TrailModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(email='username@domain.com')
        cls.start = 'Warszawa'
        cls.end = 'Gliwice'

    def test_trail_start_eq_end_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Trail(user=self.user, start=self.start, end=self.start).save()

    def test_field_validators(self):
        with self.assertRaises(ValidationError):
            Trail(user=self.user, start='Warszawa#$#$!!', end='Gliwice@#!@#!#!@').full_clean()


class WaypointModelTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(email='username@domain.com')
        self.trail = Trail.objects.create(user=user, start='Strzelce Opolskie', end='Włoszczowa Północ')

    def test_field_validators(self):
        with self.assertRaises(ValidationError):
            Waypoint(name='Gliwiiiiccee##@!#@#').full_clean()

    def test_adding_identical_waypoints_to_trail_raises_integrity_error(self):
        created_waypoints = []

        for name in ['Gliwice', 'Gliwice', 'Zabrze', 'Zawiercie']:
            created_waypoints.append(Waypoint.objects.create(name=name))

        self.trail.waypoints.add(created_waypoints[0])  # Adds 'Gliwice' waypoint
        with self.assertRaises(IntegrityError):
            self.trail.waypoints.add(created_waypoints[1]) # Tries to add 'Gliwice' waypoint, but it is forbidden.


class SentenceValidatorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.valid = 'Włosczowa'
        cls.invalid = 'Gliwice#'

        cls.many_valid = ['Włoszczowa', 'Gliwice', 'Warszawa Centralna', 'Gdańsk']
        cls.many_invalid = ['Włoszczow##a', 'Gliwice!!', 'Warszawa Centraln@@#$!a', 'Gdańsk^^^%']

    def test_valid(self):
        self.assertIsNone(validate_sentence(self.valid))

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            validate_sentence(self.invalid)

    def test_many_valid(self):
        results = [validate_sentence(valid) for valid in self.many_valid]
        self.assertTrue(all(result is None for result in results))

    def test_many_invalid(self):
        with self.assertRaises(ValidationError):
            [validate_sentence(invalid) for invalid in self.many_invalid]




