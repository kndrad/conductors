from django.urls import path

from IVU.views import (
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
