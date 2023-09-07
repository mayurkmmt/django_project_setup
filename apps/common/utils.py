import random
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.accounts.models import RegistrationOtp
from apps.common.helpers.custom_exception_helper import ExceptionError
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Util:
    @staticmethod
    def send_email(subject, recipient, message):
        message = Mail(
            from_email=settings.EMAIL_HOST_USER,
            to_emails=recipient,
            subject=subject,
            html_content=message,
        )

        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code


def create_verify_email_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    otp = random.SystemRandom().randint(100000, 999999)
    RegistrationOtp.objects.create(email=user.email, otp=otp)
    otpb64 = urlsafe_base64_encode(force_bytes(otp))
    return f"http://127.0.0.1:8000/accounts/verify-email/{uid}/{otpb64}/"
