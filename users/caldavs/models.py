import caldav
from django.conf import settings
from django.db import models

from utils.models import UUIDCommonModel


class CalDAVAccount(UUIDCommonModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='caldav_account',
        verbose_name='Użytkownik', on_delete=models.CASCADE
    )
    username = models.CharField('Login użytkownika', max_length=128)
    password = models.CharField('Hasło użytkownika', max_length=128)
    url = models.URLField('Adres URL Serwera CalDAV')

    class Meta:
        verbose_name = 'Konto CalDAV'
        verbose_name_plural = 'Konta CalDAV'

    def __repr__(self):
        return f'CalDAVAccount({self.user}, {self.username}, {self.url})'

    def __str__(self):
        return f'{self.user}: {self.url}'

    def get_client(self):
        client = caldav.DAVClient(
            url=self.url,
            username=self.username,
            password=self.password
        )
        return client
