from datetime import timedelta

from dateutil.parser import parse as dateutil_parse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from trains.searching import trains_before, DateArrivingTrain, trains_after, DateDepartingTrain
from .models import Allocation, AllocationTrain, AllocationAction
from ..api.resources import IVUAllocationActions
from ..mixins import ManageRelatedResourcesMixin


class AllocationModelViewMixin(LoginRequiredMixin, ManageRelatedResourcesMixin, View):
    model = Allocation
    context_object_name = 'allocation'
    related_model = AllocationAction
    resource_cls = IVUAllocationActions

    def add_related_resources(self, instance):
        super().add_related_resources(instance=instance)
        for action in instance.actions.all():
            date = make_aware(dateutil_parse(f'{instance.date_for_api} {action.start_hour}'))

            if date < instance.start_date:
                date += timedelta(days=1)

            action.date = date
            action.save()


class AllocationView(AllocationModelViewMixin, DetailView):
    template_name = 'allocation_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.add_related_resources(instance=self.object)
        return self.object


class UpdateAllocationView(AllocationModelViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.update_related_resources(instance=self.object)
        return redirect(self.object.get_absolute_url())


class SearchAllocationTrainViewMixin(AllocationModelViewMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def get_user_place(self, place):
        # TODO: Dodać wiadomość do templatki.
        if not self.request.user.railroad_account:
            messages.warning(
                self.request, "Aby załadować pociąg, potrzebna jest konfiguracja konta kolejowego."
            )
        else:
            return getattr(self.request.user.railroad_account, str(place).lower())


class SearchTrainBeforeAllocationView(SearchAllocationTrainViewMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        date = self.object.start_date
        departure = self.get_user_place('homeplace')
        arrival = self.get_user_place('workplace')

        trains = trains_before(date, departure, arrival)
        date = date - timedelta(minutes=self.request.user.railroad_account.administration_time)

        train = DateArrivingTrain(date).inspect(trains)
        allocation_train.before = train
        allocation_train.save()
        return redirect(self.object.get_absolute_url())


class SearchTrainAfterAllocationView(SearchAllocationTrainViewMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        date = self.object.end_date
        departure = self.get_user_place('workplace')
        arrival = self.get_user_place('homeplace')

        trains = trains_after(date, departure, arrival)
        train = DateDepartingTrain(date).inspect(trains)
        allocation_train.after = train
        allocation_train.save()
        return redirect(self.object.get_absolute_url())
