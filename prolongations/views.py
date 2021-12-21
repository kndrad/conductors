from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TicketProlongationModelForm
from .models import TicketProlongation
from utils.views import HiddenUserFormMixin


class TicketProlongationViewMixin(LoginRequiredMixin):
    model = TicketProlongation
    context_object_name = 'ticket_prolongation'


class TicketProlongationListView(TicketProlongationViewMixin, ListView):
    template_name = 'ticket_prolongation_list.html'
    context_object_name = 'ticket_prolongations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by(
            'expiration_date'
        )


class TicketProlongationCreateView(TicketProlongationViewMixin, CreateView, HiddenUserFormMixin):
    template_name = 'ticket_prolongation_form.html'
    form_class = TicketProlongationModelForm


class TicketProlongationUpdateView(TicketProlongationViewMixin, UpdateView, HiddenUserFormMixin):
    template_name = 'ticket_prolongation_form.html'
    form_class = TicketProlongationModelForm


class TicketProlongationUpdateEachToday(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        user = self.request.user
        ticket_prolongations = TicketProlongation.objects.filter(user=user)

        for ticket_prolongation in ticket_prolongations:
            ticket_prolongation.last_renewal_date = timezone.now().date()
            ticket_prolongation.save()

        path = reverse('ticket_prolongations', kwargs={'pk': user.pk})
        return redirect(path)


class TicketProlongationDeleteView(TicketProlongationViewMixin, DeleteView):
    template_name = 'ticket_prolongation_confirm_delete.html'

    def get_success_url(self):
        return reverse('ticket_prolongations', kwargs={'pk': self.request.user.pk})
