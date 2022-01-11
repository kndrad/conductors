from django.db import models


class LowercaseCharField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()
