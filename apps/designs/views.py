from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Design
from .serializers import DesignSerializer


class DesignListView(generics.ListAPIView):
    """All available designs — visible to everyone (home page)"""
    permission_classes = [AllowAny]
    serializer_class = DesignSerializer

    def get_queryset(self):
        queryset = Design.objects.filter(is_available=True).select_related('tailor__tailor_profile')
        clothing_type = self.request.query_params.get('clothing_type')
        if clothing_type:
            queryset = queryset.filter(clothing_type=clothing_type)
        return queryset.order_by('-created_at')


class TailorDesignListView(generics.ListAPIView):
    """All designs by a specific tailor"""
    permission_classes = [AllowAny]
    serializer_class = DesignSerializer

    def get_queryset(self):
        tailor_id = self.kwargs.get('tailor_id')
        return Design.objects.filter(tailor_id=tailor_id, is_available=True).order_by('-created_at')


class TailorMyDesignsView(APIView):
    """Tailor manages their own designs"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'tailor':
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        designs = Design.objects.filter(tailor=request.user).order_by('-created_at')
        serializer = DesignSerializer(designs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'tailor':
            return Response({'error': 'Only tailors can add designs.'}, status=status.HTTP_403_FORBIDDEN)
        tailor_profile = getattr(request.user, 'tailor_profile', None)
        if not tailor_profile or tailor_profile.approval_status != 'approved':
            return Response({'error': 'Your account must be approved before adding designs.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = DesignSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(tailor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TailorDesignDetailView(APIView):
    """Tailor update or delete a specific design"""
    permission_classes = [IsAuthenticated]

    def get_design(self, pk, user):
        try:
            return Design.objects.get(pk=pk, tailor=user)
        except Design.DoesNotExist:
            return None

    def put(self, request, pk):
        if request.user.role != 'tailor':
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        design = self.get_design(pk, request.user)
        if not design:
            return Response({'error': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DesignSerializer(design, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != 'tailor':
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        design = self.get_design(pk, request.user)
        if not design:
            return Response({'error': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
        design.delete()
        return Response({'message': 'Design deleted.'}, status=status.HTTP_204_NO_CONTENT)
