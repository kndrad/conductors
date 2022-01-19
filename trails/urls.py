from django.urls import path

from .views import (
    TrailListView,
    TrailCreateView,
    TrailDetailView,
    TrailUpdateView,
    TrailDeleteView,
    TrailUpdateWaypointsView,
    TrailLastDrivenTodayView,
    CalDAVSendTrails,
)

urlpatterns = [
    path('<uuid:pk>/', TrailListView.as_view(), name='trail_list'),
    path('create/', TrailCreateView.as_view(), name='trail_create'),
    path('<int:pk>/', TrailDetailView.as_view(), name='trail_detail'),
    path('update/<int:pk>/', TrailUpdateView.as_view(), name='trail_update'),
    path('delete/<int:pk>/', TrailDeleteView.as_view(), name='trail_delete'),
    path('update/waypoints/<int:pk>/', TrailUpdateWaypointsView.as_view(), name='trail_update_waypoints'),
    path('update/today/<int:pk>/', TrailLastDrivenTodayView.as_view(), name='trail_last_driven_today'),
    path('caldav/send/', CalDAVSendTrails.as_view(), name='caldav_send_trails'),
]
