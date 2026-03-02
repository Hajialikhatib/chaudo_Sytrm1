from django.urls import path
from .views import (
    UserOrdersView, UserOrderDetailView,
    TailorOrdersView, TailorOrderActionView
)

urlpatterns = [
    path('', UserOrdersView.as_view(), name='user-orders'),
    path('<int:pk>/', UserOrderDetailView.as_view(), name='order-detail'),
    path('tailor/', TailorOrdersView.as_view(), name='tailor-orders'),
    path('tailor/<int:pk>/action/', TailorOrderActionView.as_view(), name='order-action'),
]
