from django.urls import path

from .views import (
    TrailListView,
    TrailCreateView,

)

urlpatterns = [
    path('<uuid:pk>/', TrailListView.as_view(), name='trails'),
    path('create/', TrailCreateView.as_view(), name='trail_create'),
]
