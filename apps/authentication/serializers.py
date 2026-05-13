from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.persona.services import validate_custom_persona

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "language", "ai_name", "ai_persona")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah dipakai.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email sudah terdaftar.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Username atau password salah.")
        attrs["user"] = user
        return attrs


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("language", "ai_name", "ai_persona")
        extra_kwargs = {
            "language": {"required": False},
            "ai_name": {"required": False, "allow_blank": True},
            "ai_persona": {"required": False, "allow_blank": True},
        }

    def validate_ai_persona(self, value):
        result = validate_custom_persona(value)
        if not result.is_valid:
            raise serializers.ValidationError(result.message)
        return value
