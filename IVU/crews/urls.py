from django.urls import path

from .views import TrainCrewDetailView, UpdateTrainCrewView

urlpatterns = [
    path(
        '<str:train_number>/<str:date>/',
        TrainCrewDetailView.as_view(), name='train_crew_detail'
    ),
    path(
        'update/<uuid:pk>/',
        UpdateTrainCrewView.as_view(), name='update_train_crew'
    ),
]
