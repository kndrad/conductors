from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from alina.models import Allocation


class AllocationMixin(LoginRequiredMixin):
    model = Allocation
    context_object_name = 'allocation'


class AllocationView(AllocationMixin, DetailView):
    template_name = 'allocations/allocation_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.add_details_on_request(self.request)
        return self.object


class UpdateAllocationView(AllocationMixin, SingleObjectMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.update_details_on_request(self.request)
        return redirect(self.object.get_absolute_url())
