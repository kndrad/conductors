from django.urls import path

from .views import (
    AllocationView,
    UpdateAllocationView,
    SearchTrainBeforeAllocationView,
    SearchTrainAfterAllocationView
)

urlpatterns = [
    path(
        '<uuid:pk>/', AllocationView.as_view(), name='allocation_detail'
    ),
    path(
        'update/<uuid:pk>/', UpdateAllocationView.as_view(), name='update_allocation'
    ),
    path(
        'train/search/before/<uuid:pk>/',
        SearchTrainBeforeAllocationView.as_view(),
        name='search_train_before_allocation'
    ),
    path('train/search/after/<uuid:pk>/',
         SearchTrainAfterAllocationView.as_view(),
         name='search_train_after_allocation'),
]
