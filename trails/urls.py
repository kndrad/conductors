from django.urls import path

from .views import (
    TrailListView,
    TrailCreateView,

)

urlpatterns = [
    path('<uuid:pk>/', TrailListView.as_view(), name='trail_list'),
    path('create/', TrailCreateView.as_view(), name='trail_create'),
]
