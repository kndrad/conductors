from django.urls import path

from pages.views import HomePageView, AboutPageView, NotAllowedView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('not-allowed/', NotAllowedView.as_view(), name='not_allowed')
]
