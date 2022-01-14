import caldav
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.caldavs.mixins import SingleObjectCalDAVMixin
from utils.views import HiddenUserFormMixin
from .forms import ProlongationModelForm
from .models import Prolongation


class ProlongationModelViewMixin(LoginRequiredMixin):
    model = Prolongation
    context_object_name = 'prolongation'


class ProlongationListView(ProlongationModelViewMixin, ListView):
    template_name = 'prolongation_list.html'
    context_object_name = 'prolongations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('expiration_date')


class ProlongationCreateView(ProlongationModelViewMixin, CreateView, HiddenUserFormMixin):
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class ProlongationUpdateView(ProlongationModelViewMixin, UpdateView, HiddenUserFormMixin):
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class UpdateProlongationsToday(ProlongationModelViewMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = self.request.user
        prolongations = Prolongation.objects.filter(user=user)

        for prolongation in prolongations:
            prolongation.last_renewal_date = timezone.now().date()
            prolongation.save()

        url = reverse('prolongation_list', kwargs={'pk': user.pk})
        return redirect(url)


class CalDAVSendProlongations(ProlongationModelViewMixin, SingleObjectCalDAVMixin, View):
    http_method_names = ['post']

    def final_redirect(self):
        return redirect(reverse('prolongation_list', kwargs={'pk': self.request.user.pk}))

    def get_saveable_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ProlongationDeleteView(LoginRequiredMixin, DeleteView):
    model = Prolongation
    context_object_name = 'prolongation'
    template_name = 'prolongation_delete.html'

    def get_success_url(self):
        return reverse('prolongation_list', kwargs={'pk': self.request.user.pk})
