from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserManagerTest(TestCase):

    def test_create_non_password_user(self):
        user = User.objects.create_passwordless(email='username.lastname@domain.com')
        self.assertEqual(user.email, 'username.lastname@domain.com')
        self.assertEqual(user.first_name, 'Username')
        self.assertEqual(user.password, '')

    def test_manager_validates_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_passwordless(email='username')