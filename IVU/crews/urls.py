from django.urls import path

from IVU.crews.views import CrewDetailView, UpdateCrewView

urlpatterns = [
    path(
        '<str:trip>/<str:action_date>/',
        CrewDetailView.as_view(), name='crew_detail'
    ),
    path(
        'update/<uuid:pk>/',
        UpdateCrewView.as_view(), name='update_crew'
    ),
]
