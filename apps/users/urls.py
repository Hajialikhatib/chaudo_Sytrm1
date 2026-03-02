from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView, TailorRegisterView, LoginView,
    CurrentUserView, AdminUserListView, AdminTailorListView,
    AdminApproveTailorView, AdminDeleteUserView, ApprovedTailorListView
)

urlpatterns = [
    path('register/user/', UserRegisterView.as_view(), name='user-register'),
    path('register/tailor/', TailorRegisterView.as_view(), name='tailor-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', CurrentUserView.as_view(), name='current-user'),

    # Admin endpoints
    path('admin/users/', AdminUserListView.as_view(), name='admin-users'),
    path('admin/tailors/', AdminTailorListView.as_view(), name='admin-tailors'),
    path('admin/tailors/<int:tailor_id>/action/', AdminApproveTailorView.as_view(), name='admin-approve-tailor'),
    path('admin/users/<int:user_id>/delete/', AdminDeleteUserView.as_view(), name='admin-delete-user'),

    # Public
    path('tailors/', ApprovedTailorListView.as_view(), name='approved-tailors'),
]
