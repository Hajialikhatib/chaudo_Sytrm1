from django.urls import path
from .views import (
    DesignListView, TailorDesignListView,
    TailorMyDesignsView, TailorDesignDetailView
)

urlpatterns = [
    path('', DesignListView.as_view(), name='design-list'),
    path('tailor/<int:tailor_id>/', TailorDesignListView.as_view(), name='tailor-designs'),
    path('my/', TailorMyDesignsView.as_view(), name='my-designs'),
    path('my/<int:pk>/', TailorDesignDetailView.as_view(), name='design-detail'),
]
