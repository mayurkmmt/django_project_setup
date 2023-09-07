from django.urls import re_path
from .views.account_views import (
    Login,
    RegisterCompany,
    VerifyEmailAPIView,
)


urlpatterns = [
    re_path(r"^login/$", Login.as_view(), name="login"),
    re_path(r"^register/$", RegisterCompany.as_view(), name="register"),
    re_path(
        r"verify-email/$",
        VerifyEmailAPIView.as_view(),
        name="verify-otp",
    ),
]
