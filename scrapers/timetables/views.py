from datetime import timedelta

import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView

from scrapers.models import AllocationTimetable
from users.caldavs.urls import get_caldav_account_url
from utils.views import HiddenUserFormMixin
from .forms import AllocationTimetableImportForm

REQUEST_DATE_FMT = '%Y-%m-%d'


class AllocationTimetableViewMixin(LoginRequiredMixin, View):
    model = AllocationTimetable
    context_object_name = 'timetable'


class AllocationTimetableListView(AllocationTimetableViewMixin, UserPassesTestMixin, ListView):
    """Displays list of allocation timetables.
    """
    template_name = 'timetables/allocation_timetable_list.html'
    context_object_name = 'timetables'

    def test_func(self):
        has_permissions = True

        for timetable in self.get_queryset():
            has_permissions = timetable.user == self.request.user

        if not has_permissions:
            return render(
                self.request, 'timetables/allocation_timetable_not_allowed_to_view.html'
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
        path = reverse('allocation_timetables', kwargs={'pk': request.user.pk})
        return redirect(path)
