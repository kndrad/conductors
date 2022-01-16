from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from trails.models import Trail


class TrailModelMixin(LoginRequiredMixin):
    model = Trail
    context_object_name = 'trail'


class TrailListView(TrailModelMixin, ListView):
    context_object_name = 'trails'
    template_name = 'trail_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('last_driven')


class TrailCreateView(TrailModelMixin, CreateView):
    template_name = 'trail_form.html'
