import uuid

from django.db import models
from django.utils import timezone


class UUIDCommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_updated = models.DateTimeField(verbose_name='Ostatnia aktualizacja', default=timezone.now)

    class Meta:
        abstract = True

    def updated_now(self):
        self.last_updated = timezone.now()
        self.save()
        return self.last_updated

    def last_updated_local(self):
        last_updated_local = timezone.localtime(self.last_updated)
        return last_updated_local.strftime("%H:%M %d.%m.%Yr")