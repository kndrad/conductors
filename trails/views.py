from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from trails.models import Trail


class TrailListView(LoginRequiredMixin, ListView):
    model = Trail
    context_object_name = 'trails'
    template_name = 'trail_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('last_driven')


class TrailCreateView(LoginRequiredMixin, CreateView):
    model = Trail
    context_object_name = 'trail'
    template_name = 'trail_form.html'
