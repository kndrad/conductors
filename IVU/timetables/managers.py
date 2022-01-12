from django.db import models


class TimetableManager(models.Manager):

    def get_user_timetables_queryset(self, user):
        return self.model.objects.filter(user=user).all().order_by('-year', '-month')



