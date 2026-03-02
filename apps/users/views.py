from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import TailorProfile, UserProfile
from .serializers import (
    UserRegisterSerializer, TailorRegisterSerializer,
    CustomUserSerializer, LoginSerializer, TailorProfileSerializer
)

User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TailorRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TailorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Tailor registered successfully. Awaiting admin approval.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user_data = CustomUserSerializer(user).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


# ─── Admin Views ──────────────────────────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    """Get all users (admin only)"""
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role != 'admin':
            return User.objects.none()
        return User.objects.filter(role='user').select_related('user_profile')


class AdminTailorListView(generics.ListAPIView):
    """Get all tailors (admin only)"""
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.role != 'admin':
            return User.objects.none()
        return User.objects.filter(role='tailor').select_related('tailor_profile')


class AdminApproveTailorView(APIView):
    """Approve or Reject a tailor (admin only)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, tailor_id):
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')  # 'approve' or 'reject'
        try:
            tailor_profile = TailorProfile.objects.get(user_id=tailor_id)
        except TailorProfile.DoesNotExist:
            return Response({'error': 'Tailor not found.'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'approve':
            tailor_profile.approval_status = 'approved'
            tailor_profile.save()
            return Response({'message': 'Tailor approved successfully.'})
        elif action == 'reject':
            tailor_profile.approval_status = 'rejected'
            tailor_profile.save()
            return Response({'message': 'Tailor rejected.'})
        else:
            return Response({'error': 'Invalid action. Use "approve" or "reject".'}, status=status.HTTP_400_BAD_REQUEST)


class AdminDeleteUserView(APIView):
    """Delete any user or tailor (admin only)"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User deleted successfully.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class ApprovedTailorListView(generics.ListAPIView):
    """Public list of approved tailors"""
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(
            role='tailor',
            tailor_profile__approval_status='approved'
        ).select_related('tailor_profile')
