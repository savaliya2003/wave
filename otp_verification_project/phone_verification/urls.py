# phone_verification/urls.py

from django.urls import path
from .views import SendOTPAPIView, VerifyOTPAPIView

app_name = 'phone_verification'

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
]
