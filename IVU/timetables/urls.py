from django.urls import path

from .views import (
    TimetableListView,
    TimetableDetailView,
    ImportTimetableFormView,
    UpdateTimetableView,
    CalDAVSendTimetableView,
    SendAllocationsRegistersView,
)


urlpatterns = [
    path('list/<uuid:pk>/', TimetableListView.as_view(),name='timetable_list'),
    path('<uuid:pk>/', TimetableDetailView.as_view(),name='timetable_detail'),
    path('import/', ImportTimetableFormView.as_view(),name='import_timetable'),
    path('update/<uuid:pk>/', UpdateTimetableView.as_view(),name='update_timetable'),
    path('send/<uuid:pk>/', CalDAVSendTimetableView.as_view(), name='caldav_send_timetable'),
    path('send/registers/<uuid:pk>/', SendAllocationsRegistersView.as_view(), name='send_allocations_registers'),

]