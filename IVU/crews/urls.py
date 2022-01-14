from django.urls import path

from .views import TrainCrewDetailView

urlpatterns = [
    path('<str:train_number>/<str:date>/', TrainCrewDetailView.as_view(), name='train_crew_detail'),
]
