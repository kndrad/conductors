from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from utils.views import HiddenUserFormMixin

from .forms import CalDAVAccountForm
from .models import CalDAVAccount


class CalDAVAccountMixin(LoginRequiredMixin, HiddenUserFormMixin, ModelFormMixin, ProcessFormView):
    model = CalDAVAccount
    form_class = CalDAVAccountForm
    template_name = 'caldav_account_form.html'
    success_url = reverse_lazy('home')


class CalDAVAccountCreateView(CalDAVAccountMixin, CreateView):
    """CalDAVAccount create view.
    """


class CalDAVAccountUpdateView(CalDAVAccountMixin, UpdateView):
    """CalDAVAccount create view.
    """
