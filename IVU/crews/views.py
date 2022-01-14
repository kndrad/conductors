from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import TrainCrew, TrainCrewMember
from ..api.resources import IVUTrainCrew
from ..mixins import ManageRelatedResourcesMixin


class TrainCrewModelViewMixin(LoginRequiredMixin, ManageRelatedResourcesMixin, View):
    model = TrainCrew
    context_object_name = 'crew'
    related_model = TrainCrewMember
    resource_cls = IVUTrainCrew


class TrainCrewDetailView(TrainCrewModelViewMixin, DetailView):
    template_name = 'train_crew_detail.html'

    def get_object(self, queryset=None):
        train_number = self.kwargs.get('train_number')
        date = self.kwargs.get('date')

        self.object, created = self.model.objects.get_or_create(train_number=train_number, date=date)

        if created:
            self.add_related_resources(instance=self.object)
        else:
            self.update_related_resources(instance=self.object)

        return self.object
