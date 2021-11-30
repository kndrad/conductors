from django.conf import settings
from django.db import models
from django.db.models import Q, F

from utils.models import UUIDCommonModel


class RailroadAccount(UUIDCommonModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name='Konto kolejowe',
        related_name='railroad_account', null=True, blank=True, on_delete=models.CASCADE
    )
    homeplace = models.CharField('Stacja kolejowa w miejscu zamieszkania', max_length=64)
    workplace = models.CharField('Stacja kolejowa w miejscu pracy', max_length=64)

    class Meta:
        verbose_name = 'Konto kolejowe użytkownika'
        verbose_name_plural = 'Konta kolejowe użytkowników'

        constraints = [
            models.CheckConstraint(
                check=~Q(homeplace__iexact=F('workplace')), name='homeplace_not_eq_workplace'
            ),
        ]

    def __str__(self):
        return f'{self.user}, [{self.homeplace}, {self.workplace}]'

    def __repr__(self):
        return f'RailroadAccount({self.user}, {self.homeplace}, {self.workplace})'


class RailroadStation(models.Model):
    name = models.CharField('Nazwa stacji kolejowej', max_length=64, unique=True)

    class Meta:
        verbose_name = 'Stacja kolejowa'
        verbose_name_plural = 'Stacje kolejowe'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'RailroadStation({self.name})'


