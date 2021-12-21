from django.urls import path

from .views import (
    TicketProlongationListView,
    TicketProlongationCreateView,
    TicketProlongationUpdateView,
    TicketProlongationUpdateEachToday,
    TicketProlongationDeleteView,
)

urlpatterns = [
    path('<uuid:pk>/', TicketProlongationListView.as_view(), name='ticket_prolongations'),
    path('create/', TicketProlongationCreateView.as_view(), name='ticket_prolongation_create'),
    path('update/<int:pk>/', TicketProlongationUpdateView.as_view(), name='ticket_prolongation_update'),
    path('update-all/', TicketProlongationUpdateEachToday.as_view(), name='ticket_prolongation_update_each_today'),
    path('delete/<int:pk>/', TicketProlongationDeleteView.as_view(), name='ticket_prolongation_delete'),
]
