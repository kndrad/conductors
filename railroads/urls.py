from django.urls import path

from .views import RailroadAccountCreateView, RailroadAccountUpdateView, PublicRailroadTrainDetailView

urlpatterns = [
    path('account/create/', RailroadAccountCreateView.as_view(), name='create_railroad_account'),
    path('account/update/<uuid:pk>/', RailroadAccountUpdateView.as_view(), name='update_railroad_account'),
    path('train/<int:pk>/', PublicRailroadTrainDetailView.as_view(), name='train_detail')
]