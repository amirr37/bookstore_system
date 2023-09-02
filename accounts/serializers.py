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


class OTPLoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    def validate_phone_number(self, value):
        try:
            phone = CustomUser.objects.get(phone_number=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("This phone number is not registered")
        return value


class TokenResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

    def validate_user_id(self, value):
        try:
            # Check if the user with the given user_id exists
            user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist")

        # You can also perform additional validation logic here if needed

        return value




