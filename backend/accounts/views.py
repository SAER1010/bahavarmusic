from datetime import timedelta
import random
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPVerification, StudentProfile, User
from .serializers import (
    EmailLoginSerializer,
    RegisterUserSerializer,
    RequestOTPSerializer,
    StudentProfileSerializer,
    UserSerializer,
    VerifyOTPSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RequestOTPView(APIView):
    """
    Request an OTP verification code sent via SMS to the provided phone number.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        # Invalidate old unused OTPs for this number
        OTPVerification.objects.filter(phone_number=phone, is_used=False).update(is_used=True)

        # Generate a random 6-digit code (e.g. 123456 in dev or random)
        code = f"{random.randint(100000, 999999)}"
        otp = OTPVerification.objects.create(
            phone_number=phone,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        response_data = {
            'status': 'success',
            'message': 'کد تایید یکبار مصرف ارسال شد.',
            'expires_in_seconds': 120,
        }

        # Include mock code in development mode for easy testing
        if settings.DEBUG:
            response_data['mock_code'] = code

        return Response(response_data, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """
    Verify OTP code and authenticate/register the user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        otp = OTPVerification.objects.filter(
            phone_number=phone,
            code=code,
            is_used=False,
            expires_at__gte=timezone.now()
        ).first()

        if not otp:
            return Response(
                {'detail': 'کد وارد شده اشتباه است یا منقضی شده است.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark OTP as used
        otp.is_used = True
        otp.save(update_fields=['is_used'])

        # Find or create user
        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults={
                'username': f"user_{phone}",
                'is_verified': True,
            }
        )

        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=['is_verified'])

        # Ensure student profile exists
        StudentProfile.objects.get_or_create(user=user)

        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'status': 'success',
            'created': created,
            'user': user_data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)


class EmailLoginView(APIView):
    """
    Standard login with Email/Username + Password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'status': 'success',
            'user': user_data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)


class RegisterUserView(generics.CreateAPIView):
    """
    Direct user registration with Email, Username, Phone and Password.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'status': 'success',
            'user': user_data,
            'tokens': tokens,
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View and update current authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class StudentProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    View and update student musical profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile
