from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from alina.models import AllocationTimetable
from .forms import AllocationTimetableImportForm


class AllocationTimetableMixin(LoginRequiredMixin):
    model = AllocationTimetable
    context_object_name = 'timetable'


class AllocationTimetableAllocationsView(AllocationTimetableMixin, ListView):
    """Displays list of allocation timetables.
    """
    template_name = 'timetables/allocation_timetable_allocations.html'
    context_object_name = 'timetables'

    def get_queryset(self):
        timetables = self.model.objects.filter(
            user=self.request.user).all().order_by(
            '-month', '-year'
        )
        return timetables


class ImportAllocationTimetableFormView(AllocationTimetableMixin, CreateView):
    """Serves as a CreateView. Imports AllocationTimetable.
    """
    template_name = "timetables/allocation_timetable_import.html"
    form_class = AllocationTimetableImportForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'request'):
            kwargs.update({'user': self.request.user})
        return kwargs


class UpdateAllocationTimetableAllocationsView(AllocationTimetableMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_allocations_on_request(self.request)
        return redirect(self.object.get_absolute_url())
