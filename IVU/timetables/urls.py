from django.urls import path

from .views import (
    TimetableListView,
    TimetableDetailView,
    TimetableImportFormView,
    TimetableUpdateView,
    TimetableSendToCalDAVView,
    TimetableSendAllocationsRegistersView,
)

urlpatterns = [
    path('list/<uuid:pk>/', TimetableListView.as_view(), name='timetable_list'),
    path('<uuid:pk>/', TimetableDetailView.as_view(), name='timetable_detail'),
    path('import/', TimetableImportFormView.as_view(), name='import_timetable'),
    path('update/<uuid:pk>/', TimetableUpdateView.as_view(), name='update_timetable'),
    path('send/<uuid:pk>/', TimetableSendToCalDAVView.as_view(), name='caldav_send_timetable'),
    path('send/registers/<uuid:pk>/', TimetableSendAllocationsRegistersView.as_view(),
         name='send_allocations_registers'),
]
