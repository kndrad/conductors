from django.urls import path

from .views import CalDAVAccountCreateView, CalDAVAccountUpdateView

urlpatterns = [
    path('account/create/', CalDAVAccountCreateView.as_view(), name='caldav_account_create'),
    path('account/update/<uuid:pk>/', CalDAVAccountUpdateView.as_view(), name='caldav_account_update'),
]

