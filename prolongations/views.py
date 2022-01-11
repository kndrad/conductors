import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils.views import HiddenUserFormMixin
from .forms import ProlongationModelForm
from .models import Prolongation


class ProlongationListView(LoginRequiredMixin, ListView):
    model = Prolongation
    template_name = 'prolongation_list.html'
    context_object_name = 'prolongations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('expiration_date')


class ProlongationCreateView(LoginRequiredMixin, CreateView, HiddenUserFormMixin):
    model = Prolongation
    context_object_name = 'prolongation'
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class ProlongationUpdateView(LoginRequiredMixin, UpdateView, HiddenUserFormMixin):
    model = Prolongation
    context_object_name = 'prolongation'
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class UpdateProlongationsToday(LoginRequiredMixin, View):
    model = Prolongation
    context_object_name = 'prolongation'
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = self.request.user
        prolongations = Prolongation.objects.filter(user=user)

        for prolongation in prolongations:
            prolongation.last_renewal_date = timezone.now().date()
            prolongation.save()

        url = reverse('prolongation_list', kwargs={'pk': user.pk})
        return redirect(url)


class CalDAVSendProlongations(LoginRequiredMixin, View):
    model = Prolongation
    context_object_name = 'prolongation'
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = self.request.user

        if user.caldav_account:
            client = request.user.caldav_account.get_client()

            try:
                principal = client.principal()
            except caldav.error.DAVError:
                messages.error(request, "Wystąpił błąd podczas wysyłania kalendarza. Spróbuj jescze raz.")
            else:
                calendar_name = 'Prolongaty'
                try:
                    calendar = principal.calendar(name=calendar_name)
                except caldav.error.NotFoundError:
                    calendar = principal.make_calendar(name=calendar_name)

                for event in calendar.events():
                    event.delete()

                for prolongation in Prolongation.objects.filter(user=user):
                    component = prolongation.to_ical_component()
                    ical = component.to_ical()
                    calendar.save_event(ical)
        else:
            message = "Aby wysłać prolongaty do kalendarza DAV, potrzebna jest konfiguracja konta."
            messages.warning(self.request, message)

        path = reverse('prolongation_list', kwargs={'pk': request.user.pk})
        return redirect(path)


class ProlongationDeleteView(LoginRequiredMixin, DeleteView):
    model = Prolongation
    context_object_name = 'prolongation'
    template_name = 'prolongation_delete.html'

    def get_success_url(self):
        return reverse('prolongation_list', kwargs={'pk': self.request.user.pk})
