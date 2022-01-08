from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from scrapers.models import Allocation, AllocationTrain


class AllocationViewMixin(LoginRequiredMixin, View):
    model = Allocation
    context_object_name = 'allocation'


class AllocationView(AllocationViewMixin, DetailView):
    template_name = 'allocations/allocation_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.add_related_objects_on_request(self.request)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        account = 'railroad_account'
        if not hasattr(user, account):
            context[f'{account}_href'] = reverse(f'create_{account}')
        else:
            pk = getattr(user, account).pk
            context[f'{account}_href'] = reverse(f'update_{account}', kwargs={'pk': pk})

        return context


class UpdateAllocationView(AllocationViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_related_objects_on_request(self.request)
        return redirect(self.object.get_absolute_url())


class SearchAllocationTrainView(AllocationViewMixin, SingleObjectMixin):
    http_method_names = ['post']

    def get_station(self, place):
        if not self.request.user.railroad_account:
            messages.warning(
                self.request, "Aby załadować pociąg, potrzebna jest konfiguracja konta kolejowego."
            )
        else:
            return getattr(self.request.user.railroad_account, str(place).lower())


class SearchAllocationTrainBeforeAllocationView(SearchAllocationTrainView):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = request.user

        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        departure_station = self.get_station('homeplace')
        arrival_station = self.get_station('workplace')
        spare_time = user.railroad_account.spare_time

        allocation_train.search_before(departure_station, arrival_station, spare_time)
        return redirect(self.object.get_absolute_url())


class SearchAllocationTrainAfterAllocationView(SearchAllocationTrainView):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)

        departure_station = self.get_station('workplace')
        arrival_station = self.get_station('homeplace')

        allocation_train.search_after(departure_station, arrival_station, spare_time=0)
        return redirect(self.object.get_absolute_url())
