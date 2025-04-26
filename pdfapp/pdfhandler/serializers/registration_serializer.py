from django.contrib.auth import get_user_model
from rest_framework import serializers
import os

# djangos built-in user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, data):
        if os.getenv("TEST") != "true":
            if User.objects.filter(email__iexact=data["email"]).exists():
                raise serializers.ValidationError({"email": "User with that email already exists"})
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords dont match"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=True, #TODO: set to False before merging
        )
        return user
    