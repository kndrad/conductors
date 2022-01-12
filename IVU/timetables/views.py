from datetime import timedelta

import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from utils.views import HiddenUserFormMixin
from .forms import ImportTimetableForm
from .models import Timetable
from ..allocations.models import Allocation
from ..api.interfaces import IVUTimetableAllocations
from ..mixins import ModelRelatedResourcesMixin


class TimetableModelViewMixin(LoginRequiredMixin, ModelRelatedResourcesMixin):
    model = Timetable
    related_model = Allocation
    resource = IVUTimetableAllocations
    context_object_name = 'timetable'


class TimetableListView(TimetableModelViewMixin, UserPassesTestMixin, ListView):
    template_name = 'timetable_list.html'
    context_object_name = 'timetables'

    def test_func(self):
        query = self.model.objects.filter(user=self.request.user)

        if not all(timetable.user == self.request.user for timetable in query):
            return redirect('not_allowed')
        else:
            return True

    def get_queryset(self):
        present, future = timezone.now(), timezone.now() + timedelta(days=30)

        for date in [present, future]:
            timetable, created = self.model.objects.get_or_create(
                user=self.request.user, month=date.month, year=date.year
            )
            self.add_related_objects(instance=timetable)
        return self.model.objects.get_user_timetables_queryset(user=self.request.user)


class TimetableDetailView(TimetableModelViewMixin, DetailView):
    template_name = 'timetable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocations'] = self.object.allocations.all()
        return context


class ImportTimetableFormView(TimetableModelViewMixin, SuccessMessageMixin, HiddenUserFormMixin, CreateView):
    template_name = 'import_timetable_form.html'
    form_class = ImportTimetableForm
    success_message = 'Importowanie planu powiodło się.'

    def form_valid(self, form):
        self.object = form.save()
        self.add_related_objects(instance=self.object)
        return super().form_valid(form)


class UpdateTimetableView(TimetableModelViewMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.update_related_objects(instance=self.object)
        return redirect(self.object.get_absolute_url())


class CalDAVSendTimetable(LoginRequiredMixin, SingleObjectMixin, View):
    model = Timetable
    context_object_name = 'timetable'
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

                for allocation in self.object.allocations.all():
                    allocation.add_related_objects_on_request(self.request)

                    component = allocation.to_ical_component()
                    ical = component.to_ical()
                    calendar.save_event(ical)

                    if hasattr(allocation, 'trip'):
                        for train in [allocation.train_number.before, allocation.train_number.after]:
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
