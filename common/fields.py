from django.db import models


class LowerCaseCharField(models.CharField):
    """ Field for Django models that sets string value to be lowercase.
    """
    def get_prep_value(self, value):
        return str(value).lower()
