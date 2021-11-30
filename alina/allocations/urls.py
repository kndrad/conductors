from django.urls import path

from alina.allocations.views import AllocationView, UpdateAllocationView

urlpatterns = [
    path('details/<uuid:pk>/', AllocationView.as_view(), name='allocation_details'),
    path('update/<uuid:pk>/', UpdateAllocationView.as_view(), name='update_allocation'),
]
