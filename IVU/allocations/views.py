from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.timezone import make_aware, make_naive
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import Allocation, AllocationTrain, AllocationAction
from ..api.resources import IVUAllocationActions
from ..mixins import IVUModelFetchResourcesMixin
from dateutil.parser import parse as dateutil_parse


class AllocationModelViewMixin(LoginRequiredMixin, IVUModelFetchResourcesMixin, View):
    model = Allocation
    context_object_name = 'allocation'
    related_model = AllocationAction
    resource_cls = IVUAllocationActions

    def add_fetched_resources(self, instance):
        super().add_fetched_resources(instance=instance)
        for action in instance.actions.all():
            date = make_aware(
                dateutil_parse(f'{instance.start_date_str} {action.start_hour}')
            )
            if date < instance.start_date:
                date += timedelta(days=1)

            action.date = date
            action.save()


class AllocationView(AllocationModelViewMixin, DetailView):
    template_name = 'allocation_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.add_fetched_resources(instance=self.object)
        return self.object


class UpdateAllocationView(AllocationModelViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.update_fetched_resources(instance=self.object)
        return redirect(self.object.get_absolute_url())


class SearchAllocationTrainViewMixin(LoginRequiredMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def get_station(self, place):
        if not self.request.user.railroad_account:
            messages.warning(
                self.request, "Aby załadować pociąg, potrzebna jest konfiguracja konta kolejowego."
            )
        else:
            return getattr(self.request.user.railroad_account, str(place).lower())


class SearchTrainBeforeAllocationView(SearchAllocationTrainViewMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = request.user
        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        departure_station = self.get_station('homeplace')
        arrival_station = self.get_station('workplace')
        spare_time = user.railroad_account.administration_time

        # allocation_train.search_before(departure_station, arrival_station, spare_time)
        return redirect(self.object.get_absolute_url())


class SearchTrainAfterAllocationView(SearchAllocationTrainViewMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        departure_station = self.get_station('workplace')
        arrival_station = self.get_station('homeplace')

        # allocation_train.search_after(departure_station, arrival_station, spare_time=0)
        return redirect(self.object.get_absolute_url())
