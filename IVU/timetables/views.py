from datetime import timedelta

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

from users.caldavs.mixins import CalDAVSendEventsMixin
from common.views import HiddenInputUserFormMixin
from .forms import ImportTimetableForm
from .models import Timetable
from ..allocations.models import Allocation
from ..api.resources import IVUTimetableAllocations
from ..mixins import ManageRelatedResourcesMixin
from ..registers import send_allocations_registers


class TimetableModelViewMixin(LoginRequiredMixin, ManageRelatedResourcesMixin, View):
    model = Timetable
    related_model = Allocation
    resource_cls = IVUTimetableAllocations
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
            self.add_related_resources(instance=timetable)
        return self.model.objects.get_user_timetables_queryset(user=self.request.user)


class TimetableDetailView(TimetableModelViewMixin, DetailView):
    template_name = 'timetable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocations'] = self.object.allocations.all()
        return context


class TimetableImportFormView(TimetableModelViewMixin, SuccessMessageMixin, HiddenInputUserFormMixin, CreateView):
    template_name = 'import_timetable_form.html'
    form_class = ImportTimetableForm
    success_message = 'Importowanie planu powiodło się.'

    def form_valid(self, form):
        self.object = form.save()
        self.add_related_resources(instance=self.object)
        return super().form_valid(form)


class TimetableUpdateView(TimetableModelViewMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.update_related_resources(instance=self.object)
        return redirect(self.object.get_absolute_url())


class TimetableSendToCalDAVView(TimetableModelViewMixin, SingleObjectMixin, CalDAVSendEventsMixin):
    model = Timetable
    related_model = Allocation
    context_object_name = 'timetable'
    http_method_names = ['post']

    def get_query_to_send(self):
        return self.object.allocations.all()

    def calendar_name(self):
        self.object = self.get_object()
        return self.object.calendar_name

    def post_events(self):
        self.object = self.get_object()
        self.add_related_resources(instance=self.object)
        self.save_events()
        for instance in self.get_query_to_send():
            if hasattr(instance, 'train'):
                self.save_other_events([instance.train.before, instance.train.after])

    def final_redirect(self):
        return redirect(reverse('timetable_list', kwargs={'pk': self.request.user.pk}))


class TimetableSendAllocationsRegistersView(TimetableModelViewMixin, SingleObjectMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        send_allocations_registers(self.request, self.object.date_formatted)
        return redirect(self.object.get_absolute_url())
