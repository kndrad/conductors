from django.urls import path

from IVU.crews.views import TripCrewDetailView, UpdateTripCrewView

urlpatterns = [
    path(
        '<str:train_number>/<str:action_date>/',
        TripCrewDetailView.as_view(), name='train_crew_detail'
    ),
    path(
        'update/<uuid:pk>/',
        UpdateTripCrewView.as_view(), name='update_train_crew'
    ),
]
