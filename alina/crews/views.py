import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from alina.models import TrainCrew


class TrainCrewViewMixin(LoginRequiredMixin, View):
    model = TrainCrew
    context_object_name = 'train_crew'


class TrainCrewView(TrainCrewViewMixin, DetailView):
    template_name = 'train_crews/train_crew.html'

    def get_object(self, queryset=None):
        train_number = self.kwargs.get('train_number')
        formatted_action_date = self.kwargs.get('formatted_action_date')

        self.object, created = self.model.objects.get_or_create(
            train_number=train_number, date=formatted_action_date,
        )
        if created:
            self.object.add_members_on_request(self.request)

        return self.object


class UpdateTrainCrewView(TrainCrewViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_members_on_request(self.request)
        return redirect(request.META.get('HTTP_REFERER'))
