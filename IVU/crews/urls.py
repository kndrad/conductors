from django.urls import path

from IVU.crews.views import TrainCrewView, UpdateTrainCrewView

urlpatterns = [
    path(
        'members/<str:trip>/<str:formatted_action_date>/',
        TrainCrewView.as_view(), name='crew'
    ),
    path(
        'update/<uuid:pk>/',
        UpdateTrainCrewView.as_view(), name='update_crew'
    ),
]
