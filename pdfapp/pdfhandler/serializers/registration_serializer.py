from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={
            "input_type": "password"})
    password2 = serializers.CharField(
        write_only=True, required=True, style={
            "input_type": "password"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError("Password must contain at least one number")
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise serializers.ValidationError("Password must contain at least one special character")
        return password

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("User with that email already exists")
        return email

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError(
                {"password": "Passwords don't match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None) 
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False
        )
        return user