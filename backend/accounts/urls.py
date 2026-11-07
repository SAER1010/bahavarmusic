from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    EmailLoginView,
    RegisterUserView,
    RequestOTPView,
    StudentProfileUpdateView,
    UserProfileView,
    VerifyOTPView,
)

app_name = 'accounts'

urlpatterns = [
    path('otp/request/', RequestOTPView.as_view(), name='otp-request'),
    path('otp/verify/', VerifyOTPView.as_view(), name='otp-verify'),
    path('login/', EmailLoginView.as_view(), name='email-login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/student/', StudentProfileUpdateView.as_view(), name='student-profile'),
]
