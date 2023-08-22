from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from xdg.Exceptions import ValidationError

from .models import CustomUser
from accounts.models import OTPRequest


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OtpChannel.choices)

    def validate_receiver(self, value):
        # Custom validation logic for the receiver field
        if not value:
            raise ValidationError("Receiver can't be empty", file=None)
        return value


class RequestOPTResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']


class VerifyOTPRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)
