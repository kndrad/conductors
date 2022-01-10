import uuid

from django.db import models
from django.utils import timezone


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UUIDTimestampedModel(UUIDModel):
    last_updated = models.DateTimeField(
        verbose_name='Ostatnia aktualizacja', editable=False, default=timezone.now
    )

    class Meta:
        abstract = True

    def updated_now(self):
        self.last_updated = timezone.now()
        self.save()
