from django.urls import path, reverse
from .views import CalDAVAccountCreateView, CalDAVAccountUpdateView

urlpatterns = [
    path('account/create/', CalDAVAccountCreateView.as_view(), name='create_caldav_account'),
    path('account/update/<uuid:pk>/', CalDAVAccountUpdateView.as_view(), name='update_caldav_account'),
]


def get_caldav_account_url(user):
    account = 'caldav_account'
    if not hasattr(user, account):
        return reverse(f'create_{account}')
    else:
        pk = getattr(user, account).pk
        return reverse(f'update_{account}', kwargs={'pk': pk})
