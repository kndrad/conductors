from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class NotAllowedView(TemplateView):
    template_name = 'not_allowed.html'
