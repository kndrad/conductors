from django.db import models


class TimetableManager(models.Manager):

    def get_time_ordered_user_timetables(self, user):
        return self.model.objects.filter(user=user).all().order_by('-year', '-month')


