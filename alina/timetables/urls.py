from django.urls import path

from alina.timetables.views import (
    AllocationTimetableAllocationsView, ImportAllocationTimetableFormView, UpdateAllocationTimetableAllocationsView
)

urlpatterns = [
    path(
        '<uuid:pk>/', AllocationTimetableAllocationsView.as_view(),
        name='allocation_timetable_allocations'
    ),
    path(
        'import/', ImportAllocationTimetableFormView.as_view(),
        name='import_allocation_timetable'
    ),
    path(
        'update/<uuid:pk>/', UpdateAllocationTimetableAllocationsView.as_view(),
        name='update_allocations'
    ),

]
