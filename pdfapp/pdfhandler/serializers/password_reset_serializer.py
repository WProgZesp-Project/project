from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        if len(attrs['password']) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})

        if not any(char.isdigit() for char in attrs['password']):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one digit."})

        if not any(char.isupper() for char in attrs['password']):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one uppercase letter."})

        if not any(char.islower() for char in attrs['password']):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one lowercase letter."})

        if not any(not char.isalnum() for char in attrs['password']):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one special character."})

        return attrs