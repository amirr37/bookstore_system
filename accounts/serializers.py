from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from xdg.Exceptions import ValidationError

from .models import CustomUser
from accounts.models import OTPRequest


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password', 'password2', 'email']

    def validate(self, data):
        """
        Validate the password confirmation.
        """
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
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
