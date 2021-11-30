from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
