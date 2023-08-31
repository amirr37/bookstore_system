import phonenumbers
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from accounts.models import CustomUser
from accounts.models import OTPRequest
from phonenumber_field.serializerfields import PhoneNumberField


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'membership_type', 'membership_expiry_date']


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


# class RequestOTPSerializer(serializers.Serializer):
#     receiver = serializers.CharField(max_length=15)
#
#     def validate_receiver(self, value):
#         # Check if the value is a valid phone number
#         if not re.match(r'^\d{10}$', value):
#             raise serializers.ValidationError("Invalid phone number format. It should be 10 digits.")
#
#         return value
#
#
# class RequestOPTResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTPRequest
#         fields = ['request_id']
#
#
# class VerifyOTPRequestSerializer(serializers.Serializer):
#     request_id = serializers.UUIDField(allow_null=False)
#     password = serializers.CharField(max_length=4, allow_null=False)
#     receiver = serializers.CharField(max_length=64, allow_null=False)


class OTPLoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    def validate_phone_number(self, value):

        try:
            phone = CustomUser.objects.get(phone_number=value)
        except Exception:
            raise serializers.ValidationError("this phone number is not registered")
