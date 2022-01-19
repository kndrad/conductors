from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import inlineformset_factory
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from common.views import HiddenInputUserFormMixin
from trails.forms import TrailForm, WaypointForm, BaseInlineWaypointFormSet
from trails.models import Trail, Waypoint


class TrailModelMixin(LoginRequiredMixin):
    model = Trail
    context_object_name = 'trail'


class TrailListView(TrailModelMixin, ListView):
    context_object_name = 'trails'
    template_name = 'trail_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('last_driven')


class TrailDetailView(TrailModelMixin, DetailView):
    template_name = 'trail_detail.html'


class TrailFormView(TrailModelMixin, HiddenInputUserFormMixin):
    template_name = 'trail_form.html'
    form_class = TrailForm
    extra_context = {'verbose_name': Trail._meta.verbose_name}


class TrailCreateView(TrailFormView, CreateView):

    def get_success_url(self):
        return reverse('trail_update_waypoints', kwargs={'pk': self.object.pk})


class TrailUpdateView(TrailFormView, UpdateView):
    pass


class TrailDeleteView(TrailModelMixin, DeleteView):
    template_name = 'trail_delete.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        message = f'Jesteś pewien, że chcesz usunąć szlak zaczynający się od {self.object.start} do {self.object.end}'

        if self.object.waypoints.exists():
            message += " przez stacje"
            for waypoint in self.object.waypoints.all():
                message += f" {waypoint.name.title()}"
            message += '?'
        else:
            message += '?'

        context = super().get_context_data(**kwargs)
        context['message'] = message
        return context

    def get_success_url(self):
        return reverse('trail_list', kwargs={'pk': self.request.user.pk})


class TrailUpdateWaypointsView(TrailModelMixin, UpdateView):
    template_name = 'trail_waypoints_form.html'
    form_class = inlineformset_factory(
        Trail, Waypoint, fields=('name',), extra=5, max_num=5,
        form=WaypointForm, formset=BaseInlineWaypointFormSet, can_delete=False
    )

    # TODO Walidacja czy podane stacje w formularzu nie są czasem stacjami krańcowymi na szlaku

    def get_success_url(self):
        return reverse('trail_detail', kwargs={'pk': self.get_object().pk})

# TODO: Widok dla aktualizacji obiektu dzisiaj!
