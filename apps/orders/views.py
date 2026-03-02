from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer


class UserOrdersView(APIView):
    """User places and views their own orders"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'user':
            return Response({'error': 'Only users can view orders here.'}, status=403)
        orders = Order.objects.filter(user=request.user).select_related(
            'tailor__tailor_profile', 'design'
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'user':
            return Response({'error': 'Only regular users can place orders.'}, status=403)
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(
                OrderSerializer(order, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderDetailView(APIView):
    """User views a single order detail"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)


class TailorOrdersView(APIView):
    """Tailor views all orders directed to them"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'tailor':
            return Response({'error': 'Permission denied.'}, status=403)
        orders = Order.objects.filter(tailor=request.user).select_related(
            'user__user_profile', 'design'
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class TailorOrderActionView(APIView):
    """Tailor accepts or rejects an order"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != 'tailor':
            return Response({'error': 'Permission denied.'}, status=403)
        try:
            order = Order.objects.get(pk=pk, tailor=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)

        if order.status != 'pending':
            return Response({'error': 'This order has already been processed.'}, status=400)

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Order {order.status} successfully.'})
        return Response(serializer.errors, status=400)
