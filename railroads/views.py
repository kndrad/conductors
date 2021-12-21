from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from utils.views import HiddenUserFormMixin
from .forms import RailroadAccountModelForm
from .models import RailroadAccount, PublicRailroadTrain


class RailroadAccountViewMixin(LoginRequiredMixin, HiddenUserFormMixin, ModelFormMixin, ProcessFormView):
    model = RailroadAccount
    form_class = RailroadAccountModelForm
    template_name = 'railroad_account_form.html'
    success_url = reverse_lazy('home')


class RailroadAccountCreateView(RailroadAccountViewMixin, CreateView):
    """RailroadAccount create view.
    """


class RailroadAccountUpdateView(RailroadAccountViewMixin, UpdateView):
    """RailroadAccount update view.
    """


class PublicRailroadTrainDetailView(DetailView):
    model = PublicRailroadTrain
    context_object_name = 'train'
    template_name = 'train_detail.html'
