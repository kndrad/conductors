import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from utils.views import HiddenUserFormMixin
from .forms import ImportTimetableForm
from .models import Timetable


class TimetableListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Timetable
    template_name = 'timetable_list.html'
    context_object_name = 'timetables'

    def test_func(self):
        has_permissions = True

        for timetable in self.get_queryset():
            has_permissions = timetable.user == self.request.user

        if not has_permissions:
            return render(self.request, 'not_allowed_to_view.html')
        else:
            return has_permissions

    def get_queryset(self):
        request = self.request
        self.model.objects.create_present_on_request(request)
        self.model.objects.create_future_on_request(request)
        return self.model.objects.filter(user=request.user).all().order_by('-year', '-month')


class TimetableDetailView(LoginRequiredMixin, DetailView):
    model = Timetable
    context_object_name = 'timetable'
    template_name = 'timetable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocations'] = self.object.allocation_set.all()
        return context


class ImportTimetableFormView(LoginRequiredMixin, SuccessMessageMixin, HiddenUserFormMixin, CreateView):
    model = Timetable
    context_object_name = 'timetable'
    template_name = 'import_timetable_form.html'
    form_class = ImportTimetableForm
    success_message = 'Importowanie planu powiodło się.'

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class UpdateTimetableView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Timetable
    context_object_name = 'timetable'
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
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

                for allocation in self.object.allocation_set.all():
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
