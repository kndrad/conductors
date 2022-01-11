from django.db import models
from django.utils import timezone

from utils.models import UUIDModel


class UUIDTimestampedModel(UUIDModel):
    last_updated = models.DateTimeField(
        verbose_name='Ostatnia aktualizacja', editable=False, default=timezone.now
    )

    class Meta:
        abstract = True

    def update_now(self):
        self.last_updated = timezone.now()
        self.save()

