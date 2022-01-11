from django.urls import path

from .views import (
    ProlongationListView,
    ProlongationCreateView,
    ProlongationUpdateView,
    UpdateProlongationsToday,
    CalDAVSendProlongations,
    ProlongationDeleteView,
)

urlpatterns = [
    path('<uuid:pk>/', ProlongationListView.as_view(), name='prolongation_list'),
    path('create/', ProlongationCreateView.as_view(), name='prolongation_create'),
    path('update/<int:pk>/', ProlongationUpdateView.as_view(), name='prolongation_update'),
    path('update-all-today/', UpdateProlongationsToday.as_view(), name='update_prolongations_today'),
    path('caldav/send/', CalDAVSendProlongations.as_view(), name='caldav_send_prolongations'),
    path('delete/<int:pk>/', ProlongationDeleteView.as_view(), name='prolongation_delete'),
]
