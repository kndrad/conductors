from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.caldavs.mixins import CalDAVSendEventsMixin
from common.views import HiddenInputUserFormMixin
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


class ProlongationCreateView(ProlongationModelViewMixin, CreateView, HiddenInputUserFormMixin):
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class ProlongationUpdateView(ProlongationModelViewMixin, UpdateView, HiddenInputUserFormMixin):
    template_name = 'prolongation_form.html'
    form_class = ProlongationModelForm


class UpdateProlongationsToday(ProlongationModelViewMixin, View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        user = self.request.user

        for prolongation in Prolongation.objects.filter(user=user):
            prolongation.last_renewal_date = timezone.now().date()
            prolongation.save()

        return redirect(reverse('prolongation_list', kwargs={'pk': user.pk}))


class CalDAVSendProlongations(ProlongationModelViewMixin, CalDAVSendEventsMixin, View):
    http_method_names = ['post']

    def get_query_to_send(self):
        return self.model.objects.filter(user=self.request.user)

    def final_redirect(self):
        return redirect(reverse('prolongation_list', kwargs={'pk': self.request.user.pk}))

    def calendar_name(self):
        return 'Prolongaty biletów'


class ProlongationDeleteView(ProlongationModelViewMixin, DeleteView):
    template_name = 'prolongation_delete.html'

    def get_success_url(self):
        return reverse('prolongation_list', kwargs={'pk': self.request.user.pk})
