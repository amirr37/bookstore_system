from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

import accounts.SMSServices
from accounts.SMSServices import AbstractService, OTPSMSService1
from accounts.models import CustomUser, OTPRequest
from accounts.serializers import CustomUserSerializer, UserRegistrationSerializer, OTPLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.throttling import OTPLoginPostThrottle, OTPLoginPutThrottle
from accounts.circuit_breaker import CircuitBreaker
from accounts.SMSSender import SMSSender


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        'refresh': refresh_token,
        'access': access_token,
    }


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SMSServicesManagerView(APIView):
    # add services here
    sms_sender = SMSSender(accounts.SMSServices.OTPSMSService1(),
                           accounts.SMSServices.OTPSMSService2(),
                           accounts.SMSServices.OTPSMSService3(), )

    def post(self, request):
        send_message_success = self.sms_sender.execute(request)
        if send_message_success:
            return Response({'message': "otp code sent successfully"}, status=status.HTTP_200_OK)

        return Response({'message': "send otp code failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OTPVerifyView(APIView):
    # throttle_classes = [OTPLoginPutThrottle]  # Apply throttling to the PUT method

    def put(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        phone_number = request.data.get('phone_number')  # The original secret used to generate the OTP
        try:
            otp_request = OTPRequest.objects.get(phone_number=phone_number, otp_code=otp_code)
        except Exception:
            return Response({'message': 'OTP verification failed.'}, status=status.HTTP_401_UNAUTHORIZED)
        print(otp_request.expire_time)
        if otp_request.expire_time < timezone.now():
            return Response({'message': 'OTP time expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = CustomUser.objects.get(phone_number=phone_number)
            tokens = get_tokens_for_user(user)
            tokens['message'] = 'OTP verification successful. Grant access.'

            return Response(data=tokens, status=status.HTTP_200_OK)


class TokenResetView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        tokens = get_tokens_for_user(user)
        tokens['message'] = 'OTP verification successful. Grant access.'
        # Custom reset logic here
        return Response(tokens, status=status.HTTP_200_OK)


class SpecialMembershipPurchase(APIView):
    pass
