from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer
import random
from twilio.rest import Client
from django.conf import settings
import phonenumbers

class SendOTPAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        # Validate phone number
        try:
            phone_number_obj = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number_obj):
                return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
        except phonenumbers.NumberParseException:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = UserProfile.objects.get_or_create(phone_number=phone_number)

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()

        # Send OTP via Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Your OTP is: {otp}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp_entered = request.data.get('otp')

        user = UserProfile.objects.get(phone_number=phone_number)

        if otp_entered == user.otp:
            user.is_verified = True
            user.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
