from django.db import models
import uuid


class UUIDModel(models.Model):
    """ Django model with uuid id and pk.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
