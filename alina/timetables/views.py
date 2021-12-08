import caldav
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from alina.models import AllocationTimetable
from utils.views import HiddenUserFormMixin
from .forms import AllocationTimetableImportForm


class AllocationTimetableViewMixin(LoginRequiredMixin, View):
    model = AllocationTimetable
    context_object_name = 'timetable'


class AllocationTimetableAllocationsView(AllocationTimetableViewMixin, ListView):
    """Displays list of allocation timetables.
    """
    template_name = 'timetables/allocation_timetable_allocations.html'
    context_object_name = 'timetables'

    def get_queryset(self):
        timetables = self.model.objects.filter(
            user=self.request.user).all().order_by(
            '-year', '-month'
        )
        return timetables

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if not user.caldav_account:
            context['caldav_account_href'] = reverse('create_caldav_account')
        else:
            pk = user.caldav_account.pk
            context['caldav_account_href'] = reverse('update_caldav_account', kwargs={'pk': pk})

        if not user.railroad_account:
            context['railroad_account_href'] = reverse('create_railroad_account')
        else:
            pk = user.railroad_account.pk
            context['railroad_account_href'] = reverse('update_railroad_account', kwargs={'pk': pk})

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
        message = f"Przeprowadzono aktualizację harmonogramu {self.object.month}-{self.object.year}. "
        if not self.object.allocation_set.exists():
            messages.warning(
                self.request,
                message + "Niestety ten harmonogram nie posiada służb."
            )
        else:
            messages.success(
                self.request, message
            )
        return redirect(self.object.get_absolute_url())


class SendAllocationTimetableToDAVClientView(AllocationTimetableViewMixin, SingleObjectMixin):
    """Sends timetable as an calendar object to user caldav account.
    """

    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()

        if request.user.caldav_account:
            client = request.user.caldav_account.get_client()
            principal = client.principal()

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
                    if allocation.train.before:
                        train = allocation.train.before
                        component = train.get_as_ical_component()
                        ical = component.to_ical()
                        calendar.save_event(ical)

                    if allocation.train.after:
                        train = allocation.train.after
                        component = train.get_as_ical_component()
                        ical = component.to_ical()
                        calendar.save_event(ical)
        else:
            messages.warning(
                self.request, "Aby wysłać służby do serwera CalDAV, potrzebna jest konfiguracja konta."
            )
        return redirect(self.object.get_absolute_url())
