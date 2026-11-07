import re
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, OTPVerification, StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    instrument_display = serializers.CharField(source='get_instrument_display', read_only=True)
    skill_level_display = serializers.CharField(source='get_skill_level_display', read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'instrument',
            'instrument_display',
            'skill_level',
            'skill_level_display',
            'learning_goals',
            'attended_sessions_count',
            'created_at',
            'updated_at',
        ]


class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'avatar',
            'bio',
            'is_verified',
            'is_staff',
            'student_profile',
            'created_at',
        ]
        read_only_fields = ['id', 'is_staff', 'is_verified', 'created_at']

    def get_full_name(self, obj):
        name = obj.get_full_name().strip()
        return name if name else (obj.phone_number or obj.username)


class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        cleaned = re.sub(r'\s+', '', value)
        if cleaned.startswith('+98'):
            cleaned = '0' + cleaned[3:]
        elif cleaned.startswith('98'):
            cleaned = '0' + cleaned[2:]
        if not re.match(r'^09\d{9}$', cleaned):
            raise serializers.ValidationError('لطفاً یک شماره موبایل معتبر ایران (مثال: 09123456789) وارد کنید.')
        return cleaned


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        cleaned = re.sub(r'\s+', '', value)
        if cleaned.startswith('+98'):
            cleaned = '0' + cleaned[3:]
        elif cleaned.startswith('98'):
            cleaned = '0' + cleaned[2:]
        return cleaned


class EmailLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('username_or_email')
        password = attrs.get('password')

        user = authenticate(username=identifier, password=password)
        if not user:
            raise serializers.ValidationError('نام کاربری، ایمیل یا رمز عبور اشتباه است.')
        if not user.is_active:
            raise serializers.ValidationError('حساب کاربری شما غیرفعال شده است.')
        attrs['user'] = user
        return attrs


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        StudentProfile.objects.create(user=user)
        return user
