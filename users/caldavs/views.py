from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from utils.views import HiddenUserFormMixin
from .forms import CalDAVAccountModelForm
from .models import CalDAVAccount


class CalDAVAccountModelMixin(LoginRequiredMixin, HiddenUserFormMixin, ModelFormMixin, ProcessFormView):
    model = CalDAVAccount
    form_class = CalDAVAccountModelForm
    template_name = 'caldav_account_form.html'
    success_url = reverse_lazy('home')


class CalDAVAccountCreateView(CalDAVAccountModelMixin, CreateView):
    pass


class CalDAVAccountUpdateView(CalDAVAccountModelMixin, UpdateView):
    pass
