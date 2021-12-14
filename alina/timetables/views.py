from datetime import timedelta

import caldav
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.contrib import messages
from alina.models import AllocationTimetable
from utils.views import HiddenUserFormMixin
from .forms import AllocationTimetableImportForm


class AllocationTimetableViewMixin(LoginRequiredMixin, View):
    model = AllocationTimetable
    context_object_name = 'timetable'


class AllocationTimetableListView(AllocationTimetableViewMixin, ListView):
    """Displays list of allocation timetables.
    """
    template_name = 'timetables/allocation_timetable_list.html'
    context_object_name = 'timetables'

    def get_queryset(self):
        timetables = self.model.objects.filter(
            user=self.request.user).all().order_by(
            '-year', '-month'
        )
        self.create_or_update_timetables()
        return timetables

    def create_or_update_timetables(self):
        current_date = timezone.now()
        future_date = timezone.now() + timedelta(days=30)
        user = self.request.user

        for date in [current_date, future_date]:
            timetable, created = self.model.objects.get_or_create(
                user=user, month=date.month, year=date.year
            )
            if created:
                timetable.add_allocations_on_request(self.request)
            else:
                timetable.update_allocations_on_request(self.request)

        return timetable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        account = 'caldav_account'

        if not getattr(user, account):
            context[f'{account}_href'] = reverse(f'create_{account}')
        else:
            pk = getattr(user, account).pk
            context[f'{account}_href'] = reverse(f'update_{account}', kwargs={'pk': pk})

        return context


class AllocationTimetableDetailView(AllocationTimetableViewMixin, DetailView):
    template_name = 'timetables/allocation_timetable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocations'] = self.object.allocation_set.all()
        return context


class ImportAllocationTimetableFormView(
    AllocationTimetableViewMixin, SuccessMessageMixin, HiddenUserFormMixin, CreateView
):
    """Serves as a CreateView. Imports AllocationTimetable.
    """
    template_name = "timetables/allocation_timetable_import.html"
    form_class = AllocationTimetableImportForm
    success_message = "Importowanie harmonogramu powiodło się."

    def form_valid(self, form):
        self.object = form.save()
        self.object.add_allocations_on_request(self.request)
        return super().form_valid(form)


class UpdateAllocationTimetableAllocationsView(AllocationTimetableViewMixin, SingleObjectMixin):
    """Handles update of an allocation timetable on POST request.
    """
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_allocations_on_request(self.request)
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
                    allocation.add_details_on_request(self.request)

                    component = allocation.get_as_ical_component()
                    ical = component.to_ical()
                    calendar.save_event(ical)

                    if hasattr(allocation, 'train'):
                        for train in [allocation.train.before, allocation.train.after]:
                            if train:
                                component = train.get_as_ical_component()
                                ical = component.to_ical()
                                calendar.save_event(ical)
        else:
            messages.warning(
                self.request, "Aby wysłać służby do serwera CalDAV, potrzebna jest konfiguracja konta."
            )
        return redirect(self.object.get_absolute_url())
