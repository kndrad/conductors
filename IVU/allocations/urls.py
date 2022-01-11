from django.urls import path

from .views import (
    AllocationTimetableListView,
    AllocationTimetableDetailView,
    ImportAllocationTimetableFormView,
    UpdateAllocationTimetableAllocationsView,
    SendAllocationTimetableToDAVClientView
)

urlpatterns = [
    path(
        '<uuid:pk>/', AllocationTimetableListView.as_view(),
        name='allocation_timetables'
    ),
    path(
        'timetable/<uuid:pk>/', AllocationTimetableDetailView.as_view(),
        name='timetable_allocations'
    ),
    path(
        'import/', ImportAllocationTimetableFormView.as_view(),
        name='import_allocation_timetable'
    ),
    path(
        'update/<uuid:pk>/', UpdateAllocationTimetableAllocationsView.as_view(),
        name='update_timetable_allocations'
    ),
    path(
        'send/<uuid:pk>/', SendAllocationTimetableToDAVClientView.as_view(),
        name='send_allocation_timetable_to_dav_client',
    ),

]

urlpatterns = [
    path(
        'details/<uuid:pk>/', AllocationView.as_view(), name='allocation_detail'
    ),
    path(
        'update/<uuid:pk>/', UpdateAllocationView.as_view(), name='update_allocation'
    ),
    path(
        'train/heading/<uuid:pk>/',
        SearchAllocationTrainBeforeAllocationView.as_view(),
        name='search_train_before_allocation'
    ),
    path('train/returning/<uuid:pk>/',
         SearchAllocationTrainAfterAllocationView.as_view(),
         name='search_train_after_allocation'),
]

