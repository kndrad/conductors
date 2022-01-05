from django.urls import path

from facades.allocations.views import (
    AllocationView,
    UpdateAllocationView,
    SearchAllocationTrainBeforeAllocationView,
    SearchAllocationTrainAfterAllocationView
)

urlpatterns = [
    path(
        'details/<uuid:pk>/', AllocationView.as_view(), name='allocation_detail'
    ),
    path(
        'update/<uuid:pk>/', UpdateAllocationView.as_view(), name='update_allocation'
    ),
    path(
        'train/before/<uuid:pk>/',
        SearchAllocationTrainBeforeAllocationView.as_view(),
        name='search_train_before_allocation'
    ),
    path('train/after/<uuid:pk>/',
         SearchAllocationTrainAfterAllocationView.as_view(),
         name='search_train_after_allocation'),
]
