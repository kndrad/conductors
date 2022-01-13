from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import TrainCrew, TrainCrewMember
from ..api.resources import IVUTrainCrew
from ..mixins import IVUModelFetchResourcesMixin


class TrainCrewModelViewMixin(LoginRequiredMixin, IVUModelFetchResourcesMixin, View):
    model = TrainCrew
    context_object_name = 'crew'
    related_model = TrainCrewMember
    resource_cls = IVUTrainCrew


class TrainCrewDetailView(TrainCrewModelViewMixin, DetailView):
    template_name = 'train_crew_detail.html'

    def get_object(self, queryset=None):
        train_number = self.kwargs.get('train_number')
        date = self.kwargs.get('date')

        self.object, created = self.model.objects.get_or_create(
            train_number=train_number, date=date
        )

        if created:
            self.add_fetched_resources(instance=self.object)

        return self.object


class UpdateTrainCrewView(TrainCrewModelViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.update_fetched_resources(instance=self.object)
        return redirect(request.META.get('HTTP_REFERER'))
