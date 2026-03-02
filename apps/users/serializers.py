from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile, TailorProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'], write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'full_name', 'location', 'phone_number', 'gender', 'email']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        location = validated_data.pop('location')
        phone_number = validated_data.pop('phone_number')
        gender = validated_data.pop('gender')
        email = validated_data.pop('email', '')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email,
            role='user',
        )
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            location=location,
            phone_number=phone_number,
            gender=gender,
            email=email,
        )
        return user


class TailorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    clothing_type = serializers.ChoiceField(
        choices=['male', 'female', 'both'], write_only=True
    )
    bio = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'full_name', 'location', 'phone_number', 'clothing_type', 'bio']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        location = validated_data.pop('location')
        phone_number = validated_data.pop('phone_number')
        clothing_type = validated_data.pop('clothing_type')
        bio = validated_data.pop('bio', '')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role='tailor',
        )
        TailorProfile.objects.create(
            user=user,
            full_name=full_name,
            location=location,
            phone_number=phone_number,
            clothing_type=clothing_type,
            bio=bio,
            approval_status='pending',
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TailorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TailorProfile
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    tailor_profile = TailorProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined', 'user_profile', 'tailor_profile']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Invalid credentials. Please try again.')
        if not user.is_active:
            raise serializers.ValidationError('Your account has been deactivated.')
        if user.role == 'tailor':
            tailor_profile = getattr(user, 'tailor_profile', None)
            if tailor_profile and tailor_profile.approval_status == 'pending':
                raise serializers.ValidationError('Your account is awaiting admin approval.')
            if tailor_profile and tailor_profile.approval_status == 'rejected':
                raise serializers.ValidationError('Your account has been rejected by admin.')
        return {'user': user}
