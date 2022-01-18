from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from trails.forms import WaypointForm, TrailForm
from trails.models import Trail
from common.views import HiddenInputUserFormMixin


class TrailModelMixin(LoginRequiredMixin):
    model = Trail
    context_object_name = 'trail'


class TrailListView(TrailModelMixin, ListView):
    context_object_name = 'trails'
    template_name = 'trail_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('last_driven')


class TrailCreateView(TrailModelMixin, HiddenInputUserFormMixin, CreateView):
    template_name = 'trail_form.html'
    form_class = TrailForm

    def get_success_url(self):
        return reverse('trail_list', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['waypoint_formset'] = formset_factory(WaypointForm, extra=5)
        return context
