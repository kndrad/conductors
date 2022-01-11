import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):

    def create_passwordless(self, email=None, **kwargs):
        """Creates user without any password. Only with email, username and first_name.
        """
        validate_email(email)

        username, _ = str(email).rsplit('@', 1)
        first_name = (username.split('.', 1)[0] or username).title()

        user = self.model(
            email=email, username=username, first_name=first_name, **kwargs
        )

        user.save()
        return user

    @classmethod
    def get_or_create_passwordless(cls, email=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_passwordless(email=email, **kwargs)
            return user
        else:
            return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(_('password'), max_length=128, null=True, blank=True, default="")

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_and_username',
            ),
        ]

    def __str__(self):
        return self.email

    def __repr__(self):
        return f'User({self.email})'

    def get_account_url(self, account):
        if not hasattr(self, account):
            return reverse(f'{account}_create')
        else:
            pk = getattr(self, account).pk
            return reverse(f'{account}_update', kwargs={'pk': pk})

    @property
    def caldav_account_url(self):
        return self.get_account_url('caldav_account')

    @property
    def railroad_account_url(self):
        return self.get_account_url('railroad_account')
