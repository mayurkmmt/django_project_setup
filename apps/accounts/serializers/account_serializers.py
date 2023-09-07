from rest_framework import serializers
from apps.accounts.models import Company, User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from apps.common.helpers.custom_exception_helper import ExceptionError
from apps.common.constant import ErrorMsg
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def is_valid(self, raise_exception=False):
        email = self.initial_data.get("email", None)
        try:
            validate_email(email)
        except:
            raise ExceptionError(ErrorMsg.INVALID_EMAIL)
        return super(LoginSerializer, self).is_valid(raise_exception)

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise ExceptionError(ErrorMsg.USER_NOT_FOUND)

        if not user.is_active:
            raise ExceptionError(ErrorMsg.NOT_ACTIVATE_ACCOUNT)

        if not user.is_verified:
            raise ExceptionError(ErrorMsg.ACCOUNT_NOT_VERIFIED)
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise ExceptionError(ErrorMsg.INVALID_CREDENTIALS)

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"write_only": True},
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def is_valid(self, raise_exception=False):
        email = self.initial_data.get("email", None)
        try:
            validate_email(email)
        except:
            raise ExceptionError(ErrorMsg.INVALID_EMAIL)
        return super(UserSerializer, self).is_valid(raise_exception)
