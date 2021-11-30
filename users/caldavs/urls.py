from django.urls import path
from .views import CalDAVAccountCreateView, CalDAVAccountUpdateView


urlpatterns = [
    path('create/', CalDAVAccountCreateView.as_view(), name='create_caldav_account'),
    path('update/<uuid:pk>/', CalDAVAccountUpdateView.as_view(), name='update_caldav_account'),
]