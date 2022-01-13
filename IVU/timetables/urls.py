from django.urls import path

from .views import (
    TimetableListView,
    TimetableDetailView,
    ImportTimetableFormView,
    UpdateTimetableView,
    CalDAVSendTimetable,
)


urlpatterns = [
    path(
        'list/<uuid:pk>/', TimetableListView.as_view(),
        name='timetable_list'
    ),
    path(
        '<uuid:pk>/', TimetableDetailView.as_view(),
        name='timetable_detail'
    ),
    path(
        'import/', ImportTimetableFormView.as_view(),
        name='import_timetable'
    ),
    path(
        'update/<uuid:pk>/', UpdateTimetableView.as_view(),
        name='update_timetable'
    ),
    path(
        'send/<uuid:pk>/', CalDAVSendTimetable.as_view(),
        name='caldav_send_timetable',
    ),

]