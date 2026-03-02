from rest_framework import serializers
from .models import Order
from apps.designs.serializers import DesignSerializer


class OrderSerializer(serializers.ModelSerializer):
    design_detail = DesignSerializer(source='design', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    tailor_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'tailor', 'design', 'design_detail',
            'order_type', 'quantity', 'notes',
            'custom_design_image', 'custom_description',
            'status', 'rejection_reason',
            'user_full_name', 'tailor_full_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'status', 'rejection_reason', 'created_at', 'updated_at']

    def get_user_full_name(self, obj):
        profile = getattr(obj.user, 'user_profile', None)
        return profile.full_name if profile else obj.user.username

    def get_tailor_full_name(self, obj):
        profile = getattr(obj.tailor, 'tailor_profile', None)
        return profile.full_name if profile else obj.tailor.username


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['tailor', 'design', 'order_type', 'quantity', 'notes', 'custom_design_image', 'custom_description']

    def validate(self, data):
        order_type = data.get('order_type', 'design')
        if order_type == 'design' and not data.get('design'):
            raise serializers.ValidationError({'design': 'Design is required for standard orders.'})
        if order_type == 'custom' and not data.get('custom_description'):
            raise serializers.ValidationError({'custom_description': 'Description is required for custom orders.'})
        return data


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'rejection_reason']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected', 'completed']:
            raise serializers.ValidationError('Invalid status.')
        return value
