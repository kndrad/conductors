from django.urls import path

from .views import RailroadAccountCreateView, RailroadAccountUpdateView, TrainDetailView

urlpatterns = [
    path('account/create/', RailroadAccountCreateView.as_view(), name='railroad_account_create'),
    path('account/update/<uuid:pk>/', RailroadAccountUpdateView.as_view(), name='railroad_account_update'),
    path('train/<int:pk>/', TrainDetailView.as_view(), name='train_detail')
]