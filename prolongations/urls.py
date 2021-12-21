from django.urls import path

from .views import (
    TicketProlongationListView,
)

urlpatterns = [
    path('<uuid:pk>/', TicketProlongationListView.as_view(), name='ticket_prolongations'),
]
