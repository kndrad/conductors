from django.urls import path

from pages.views import HomePageView, NotAllowedView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('not-allowed/', NotAllowedView.as_view(), name='not_allowed')
]
