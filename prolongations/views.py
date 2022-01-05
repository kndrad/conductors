import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.caldavs.urls import get_caldav_account_url
from utils.views import HiddenUserFormMixin
from .forms import TicketProlongationModelForm
from .models import TicketProlongation


class TicketProlongationViewMixin(LoginRequiredMixin):
    model = TicketProlongation
    context_object_name = 'ticket_prolongation'


class TicketProlongationListView(TicketProlongationViewMixin, ListView):
    template_name = 'ticket_prolongation_list.html'
    context_object_name = 'ticket_prolongations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('expiration_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caldav_account_href'] = get_caldav_account_url(self.request.user)
        return context


class TicketProlongationCreateView(TicketProlongationViewMixin, CreateView, HiddenUserFormMixin):
    template_name = 'ticket_prolongation_form.html'
    form_class = TicketProlongationModelForm


class TicketProlongationUpdateView(TicketProlongationViewMixin, UpdateView, HiddenUserFormMixin):
    template_name = 'ticket_prolongation_form.html'
    form_class = TicketProlongationModelForm


class TicketProlongationUpdateEachToday(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = self.request.user
        prolongations = TicketProlongation.objects.filter(user=user)

        for prolongation in prolongations:
            prolongation.last_renewal_date = timezone.now().date()
            prolongation.save()

        url = reverse('ticket_prolongations', kwargs={'pk': user.pk})
        return redirect(url)


class SendTicketProlongationsToDAVClientView(LoginRequiredMixin, View):
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
                calendar_name = 'Prolongaty biletów'
                try:
                    calendar = principal.calendar(name=calendar_name)
                except caldav.error.NotFoundError:
                    calendar = principal.make_calendar(name=calendar_name)

                for event in calendar.events():
                    event.delete()

                for ticket_prolongation in TicketProlongation.objects.filter(user=user):
                    component = ticket_prolongation.get_as_ical_component()
                    ical = component.to_ical()
                    calendar.save_event(ical)
        else:
            message = "Aby wysłać prolongaty do kalendarza DAV, potrzebna jest konfiguracja konta."
            messages.warning(self.request, message)

        path = reverse('ticket_prolongations', kwargs={'pk': request.user.pk})
        return redirect(path)


class TicketProlongationDeleteView(TicketProlongationViewMixin, DeleteView):
    template_name = 'ticket_prolongation_confirm_delete.html'

    def get_success_url(self):
        return reverse('ticket_prolongations', kwargs={'pk': self.request.user.pk})
