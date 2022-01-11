from datetime import timedelta

import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from IVU.allocations.forms import ImportAllocationTimetableForm
from users.caldavs.urls import get_caldav_account_url
from utils.views import HiddenUserFormMixin
from .models import Allocation
from .models import AllocationTimetable


class AllocationTimetableViewMixin(LoginRequiredMixin, View):
    model = AllocationTimetable
    context_object_name = 'timetable'


class AllocationTimetableListView(AllocationTimetableViewMixin, UserPassesTestMixin, ListView):
    """Displays list of allocation timetables.
    """
    template_name = 'allocation_timetable_list.html'
    context_object_name = 'timetables'

    def test_func(self):
        has_permissions = True

        for timetable in self.get_queryset():
            has_permissions = timetable.user == self.request.user

        if not has_permissions:
            return render(
                self.request, 'allocation_timetable_not_allowed_to_view.html'
            )
        else:
            return has_permissions

    def get_queryset(self):
        timetables = self.model.objects.filter(user=self.request.user).all().order_by('-year', '-month')
        return timetables

    def create_or_update_timetables(self):
        user = self.request.user
        future_date = timezone.now() + timedelta(days=30)

        for date in [timezone.now(), future_date]:
            timetable, created = self.model.objects.get_or_create(
                user=user, month=date.month, year=date.year
            )
            if created:
                timetable.add_related_objects_on_request(self.request)
            else:
                timetable.update_related_objects_on_request(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.create_or_update_timetables()
        context['caldav_account_href'] = get_caldav_account_url(self.request.user)
        return context


class AllocationTimetableDetailView(AllocationTimetableViewMixin, DetailView):
    template_name = 'allocation_timetable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocations'] = self.object.allocation_set.all()
        return context


class ImportAllocationTimetableFormView(
    AllocationTimetableViewMixin, SuccessMessageMixin, HiddenUserFormMixin, CreateView
):
    """Serves as a CreateView. Imports IVUTimetableAllocationsResource.
    """
    template_name = "allocation_timetable_import.html"
    form_class = ImportAllocationTimetableForm
    success_message = "Importowanie harmonogramu powiodło się."

    def form_valid(self, form):
        self.object = form.save()
        self.object.add_related_objects_on_request(self.request)
        return super().form_valid(form)


class UpdateAllocationTimetableAllocationsView(AllocationTimetableViewMixin, SingleObjectMixin):
    """Handles update of an allocation timetable on POST request.
    """
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_related_objects_on_request(self.request)
        return redirect(self.object.get_absolute_url())


class SendAllocationTimetableToDAVClientView(AllocationTimetableViewMixin, SingleObjectMixin):
    """Sends timetable as an calendar object to user caldav account.
    """

    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()

        if request.user.caldav_account:
            client = request.user.caldav_account.get_client()

            try:
                principal = client.principal()
            except caldav.error.DAVError:
                messages.error(request, "Wystąpił błąd podczas wysyłania kalendarza. Spróbuj jescze raz.")
            else:
                try:
                    calendar = principal.calendar(name=self.object.name)
                except caldav.error.NotFoundError:
                    calendar = principal.make_calendar(name=self.object.name)

                for event in calendar.events():
                    event.delete()

                for allocation in self.object.allocation_set.all():
                    allocation.add_related_objects_on_request(self.request)

                    component = allocation.to_ical_component()
                    ical = component.to_ical()
                    calendar.save_event(ical)

                    if hasattr(allocation, 'trip'):
                        for train in [allocation.train_number.heading, allocation.train_number.returning]:
                            if train:
                                component = train.to_ical_component()
                                ical = component.to_ical()
                                calendar.save_event(ical)
        else:
            messages.warning(
                self.request, "Aby wysłać służby do serwera CalDAV, potrzebna jest konfiguracja konta."
            )
        path = reverse('allocation_timetables', kwargs={'pk': request.user.pk})
        return redirect(path)


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


# class SearchAllocationTrainView(AllocationViewMixin, SingleObjectMixin):
#     http_method_names = ['post']
#
#     def get_station(self, place):
#         if not self.request.user.railroad_account:
#             messages.warning(
#                 self.request, "Aby załadować pociąg, potrzebna jest konfiguracja konta kolejowego."
#             )
#         else:
#             return getattr(self.request.user.railroad_account, str(place).lower())
#
#
# class SearchAllocationTrainBeforeAllocationView(SearchAllocationTrainView):
#     http_method_names = ['post']
#
#     def post(self, request, **kwargs):
#         user = request.user
#
#         self.object = self.get_object()
#         allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)
#
#         departure_station = self.get_station('homeplace')
#         arrival_station = self.get_station('workplace')
#         spare_time = user.railroad_account.administration_time
#
#         allocation_train.search_before(departure_station, arrival_station, spare_time)
#         return redirect(self.object.get_absolute_url())
#
#
# class SearchAllocationTrainAfterAllocationView(SearchAllocationTrainView):
#     http_method_names = ['post']
#
#     def post(self, request, **kwargs):
#         self.object = self.get_object()
#         allocation_train, _ = AllocationTrain.objects.get_or_create(allocation=self.object)
#
#         departure_station = self.get_station('workplace')
#         arrival_station = self.get_station('homeplace')
#
#         allocation_train.search_after(departure_station, arrival_station, spare_time=0)
#         return redirect(self.object.get_absolute_url())
