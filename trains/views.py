from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from common.views import HiddenInputUserFormMixin
from .forms import RailroadAccountModelForm
from .models import RailroadAccount, Train


class RailroadAccountViewMixin(LoginRequiredMixin, HiddenInputUserFormMixin, ModelFormMixin, ProcessFormView):
    model = RailroadAccount
    form_class = RailroadAccountModelForm
    template_name = 'railroad_account_form.html'
    success_url = reverse_lazy('home')


class RailroadAccountCreateView(RailroadAccountViewMixin, CreateView):
    pass


class RailroadAccountUpdateView(RailroadAccountViewMixin, UpdateView):
    pass


class TrainDetailView(DetailView):
    model = Train
    context_object_name = 'train'
    template_name = 'train_detail.html'
