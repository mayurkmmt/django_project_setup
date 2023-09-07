from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Company, RegistrationOtp, User
from apps.accounts.serializers.account_serializers import (
    LoginSerializer,
    UserSerializer,
)
from apps.common.constant import ErrorMsg, SystemMsg
from apps.common.helpers.error_decorator_helper import track_error
from apps.common.utils import Util, create_verify_email_link
from django_demo.jwt_custom_token import get_tokens_for_user


# Create your views here.
class Login(APIView):
    permission_classes = (AllowAny,)

    @track_error(validate_api_parameters=["email", "password"])
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user=user)

        return Response(
            {
                "error": False,
                "message": SystemMsg.LOGIN_SUCCESS,
                "email": request.data.get("email"),
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class RegisterCompany(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @track_error(
        validate_api_parameters=[
            "company_name",
            "email",
            "first_name",
            "last_name",
            "password",
        ]
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request_data = request.data
        company, _ = Company.objects.get_or_create(
            company_name=request_data.get("company_name"),
            company_email=request_data.get("email"),
        )
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save(
            company_id=company.id,
            is_company_admin=True,
            password=make_password(request_data.get("password")),
        )
        verify_link = create_verify_email_link(user=user_data)
        Util.send_email(
            subject="Verify user",
            recipient=user_data.email,
            message=f"Click here to verify your account {verify_link}",
        )

        return Response(
            {
                "data": {
                    "first_name": user_data.first_name,
                    "last_name": user_data.last_name,
                    "email": user_data.email,
                    "is_verified": user_data.is_verified,
                },
                "message": SystemMsg.COMPANY_CREATED_SUCCESS,
                "error": False,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailAPIView(APIView):
    """
    This view is used to verify the OTP sent to the user's email during registration process.
    """

    permission_classes = (AllowAny,)

    @track_error(validate_api_parameters=["useridb64", "otpb64"])
    def post(self, request, *args, **kwargs):
        useridb64, otpb64 = request.data.get("useridb64"), request.data.get("otpb64")
        user_id, otp = urlsafe_base64_decode(useridb64).decode(
            "utf-8"
        ), urlsafe_base64_decode(otpb64).decode("utf-8")
        user = User.objects.get(id=user_id)
        registration_otp = RegistrationOtp.objects.filter(
            email=user.email, is_active=True, otp=otp
        ).first()
        if registration_otp and registration_otp.otp == otp:
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            tokens = get_tokens_for_user(user=user)
            registration_otp.is_active = False
            registration_otp.save(update_fields=["is_active"])
            return Response(
                data={
                    "error": False,
                    "data": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "user": user.email,
                        "company_name": user.company.company_name,
                        "is_verified_user": user.is_verified,
                        "tokens": tokens,
                    },
                    "message": SystemMsg.EMAIL_VERIFIED_SUCCESS,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    "error": True,
                    "data": {"is_valid_otp": False},
                    "message": ErrorMsg.EMAIL_VERIFICATION_FAILED,
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
