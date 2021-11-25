from django.urls import path

from alina.crews.views import TrainCrewView, UpdateTrainCrewView

urlpatterns = [
    path(
        'members/<str:train_number>/<str:formatted_action_date>/',
        TrainCrewView.as_view(), name='train_crew'
    ),
    path(
        'update/<uuid:pk>/',
        UpdateTrainCrewView.as_view(), name='update_train_crew'
    ),
]
