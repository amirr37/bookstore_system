from accounts.models import OTPRequest
from accounts.serializers import OTPLoginSerializer


def generate_otp(request):
    serializer = OTPLoginSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp_request = OTPRequest(phone_number=phone_number)
        otp_request.save()
        return otp_request
    else:
        return serializer.errors
