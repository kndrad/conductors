from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import TrainCrew


class TripCrewDetailView(LoginRequiredMixin, DetailView):
    model = TrainCrew
    template_name = 'train_crew_detail.html'
    context_object_name = 'crew'

    def get_object(self, queryset=None):
        train_number = self.kwargs.get('train_number')
        date = self.kwargs.get('action_date')

        self.object, created = self.model.objects.get_or_create(
            train_number=train_number, date=date
        )

        if created:
            self.object.add_related_objects_on_request(self.request)

        return self.object


class UpdateTripCrewView(LoginRequiredMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_related_objects_on_request(self.request)
        return redirect(request.META.get('HTTP_REFERER'))
