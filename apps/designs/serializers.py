from rest_framework import serializers
from .models import Design


class DesignSerializer(serializers.ModelSerializer):
    tailor_name = serializers.SerializerMethodField()
    tailor_location = serializers.SerializerMethodField()

    class Meta:
        model = Design
        fields = [
            'id', 'tailor', 'tailor_name', 'tailor_location',
            'title', 'description', 'clothing_type',
            'price', 'image', 'is_available', 'created_at'
        ]
        read_only_fields = ['tailor', 'created_at']

    def get_tailor_name(self, obj):
        profile = getattr(obj.tailor, 'tailor_profile', None)
        return profile.full_name if profile else obj.tailor.username

    def get_tailor_location(self, obj):
        profile = getattr(obj.tailor, 'tailor_profile', None)
        return profile.location if profile else ''
